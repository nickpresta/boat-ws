import elixir
from random import choice
import sqlalchemy
import threading
import time

from twisted.internet import reactor
from twisted.python import log

from attack_controller import AttackController
from io_controller import IOController
from movement_controller import MovementController
from models import *
from player import Player, PlayerStatus

elixir.setup_all(True)
elixir.session.configure(autocommit=True, autoflush=True)

class Game(object):
    """ The Game class is responsible for delegating tasks to the appropriate controllers as well as storing Player information """

    def __init__(self, map, max_players):
        """ We initialize an action map that we use to automatically call the methods based on the attacks """
        self.actions = {'playerName': self._player_name,
                        'fireBroadside': self._fire_broadside,
                        'changeSpeed': self._change_speed,
                        'changeHeading': self._change_heading,
                        'gameSurrender': self._game_surrender,
                        'repair': self._repair}
        self.update_timeout = 0.3 # in seconds

        self.active_players = []
        self.inactive_players = []

        try:
            self.all_ships = Ship.query.all()
        except sqlalchemy.orm.exc.NoResultFound:
            # Create a single default ship
            self.all_ships = [Ship(hit_points=100, max_hit_points=100, max_speed=200, num_cannons=10,
                ship_type=ShipType.CORVETTE, name=u"HMS Surprise",
                max_theta=180, max_ratio=2, turn_radius_factor=1,
                sails=0.0)]

        try:
            self.map = Map.query.filter_by(name=unicode(map)).one()
        except sqlalchemy.orm.exc.NoResultFound:
            self.map = Map(name=u"DEFAULT", x=2000, y=2000, wind_speed=25, wind_dir=0,
                    rain=0.0, fog=400, waves=0.0)

        self.io_controller = IOController()
        self.attack_controller = AttackController()
        self.movement_controller = MovementController(self.map)

        self.max_players = max_players

        self.response = None
        self.thread_started = False
        self.ready_players = 0
        self.gameFinished = False

    def send_message(self, client, message):
        """ This method takes a client (who sent the message) and the message they sent """

        client.broadcast("FOOBAR!")

        try:
            parsed = self.io_controller.parse_message(message)
        except IndexError:
            return
        command = parsed['command']
        args = parsed['args']

        try:
            calling_player = [p for p in self.active_players if p.id == client.id][0]
        except IndexError:
            client.broadcast("Player '%d' not found" % client.id)

        try:
            self.actions[command](calling_player, args)
        except KeyError:
            client.broadcast("Command '%s' not found. '%s' in actions = %s" % (command, command,
                    command in self.actions))

    def run(self):
        """ This method starts a Thread, which updates the positions on all players """
        log.msg("Starting thread!")

        threading.Thread(target=self._update).start()

    def stop_turning_player(self, *args):
        args[0].is_turning = False

    def stop_repairing(self, *args):
        args[0].is_repairing = False

    def _update(self):
        """ This method is being run in a Thread. It is responsible for checking the clients list and updating all player positions in that list """
        log.msg("Starting update loop")
        sent_finished_game = False
        while True:
            # get the position of all active players
            for p in self.active_players:
                if p.requested_heading == 0:
                    try:
                        self.movement_controller.update_position(p, p.heading, self.update_timeout, self.active_players)
                    except:
                        pass
                else:
                    time_took = self.movement_controller.update_turning(p, p.requested_heading)
                    threading.Timer(time_took, self.stop_turning_player, (p,)).start()

                if p.is_turning or p.is_repairing:
                    continue

                if p.player_state == PlayerStatus.SUNK:
                    self.player_sunk(p)

                status_msg = self.io_controller.build_message({'command':'shipStatus','args': [p.id, p.ship.hit_points / p.ship.max_hit_points, p.player_state]})
                state_msg = self.io_controller.build_message({'command': 'shipState',
                    'args': [p.id, int(p.position[0]), int(p.position[1]), int(p.heading)]})

                # send this message to all players (active and inactive)
                for p in self.active_players + self.inactive_players:
                    if self.victor() and not sent_finished_game:
                        victor_message = self.io_controller.build_message({'command': 'gameFinished',
                            'args': [self.active_players[0].id]})
                        reactor.callFromThread(p.client.broadcast, victor_message)

                    if p.player_state == PlayerStatus.SUNK:
                        reactor.callFromThread(p.client.broadcast, status_msg)

                    reactor.callFromThread(p.client.broadcast, state_msg)

                if self.victor():
                    sent_finished_game = True
                if not self.active_players:
                    sent_finished_game = False

            time.sleep(self.update_timeout)

    def _send_init(self, player):
        """ Sends all the playerShip and otherShip messages to all players """

        other_players = [p for p in self.active_players if player.id != p.id]
        for p in other_players:
            other_ship_msg = self.io_controller.build_message({'command': 'otherShip',
                'args': [p.id, p.ship.max_theta, p.ship.turn_radius_factor,
                    p.ship.max_ratio, p.name]})
            player.client.broadcast(other_ship_msg)
        for p in other_players:
            other_ship_msg = self.io_controller.build_message({'command': 'otherShip',
                'args': [player.id, p.ship.max_theta, p.ship.turn_radius_factor,
                    p.ship.max_ratio, player.name]})
            p.client.broadcast(other_ship_msg)

    def _player_name(self, calling_player, args):
        calling_player.name = str(args[0])
        # Create a new field in the scores table
        all_scores = Scores.query.all()
        try:
            player_field = [p for p in all_scores if calling_player.name == p.player_name][0]
        except IndexError:
            elixir.session.begin()
            Scores(player_name=unicode(calling_player.name), wins=0, losses=0, surrenders=0)
            elixir.session.commit()

        self.ready_players += 1

        # send init data to client
        map_msg = self.io_controller.build_message({'command': 'mapSize',
            'args': [self.map.x, self.map.y]})
        wind_msg = self.io_controller.build_message({'command': 'wind',
            'args': [self.map.wind_speed, self.map.wind_dir]})
        player_ship_msg = self.io_controller.build_message({'command': 'playerShip',
            'args': [calling_player.id, calling_player.ship.max_theta, calling_player.ship.turn_radius_factor,
                calling_player.ship.max_ratio, calling_player.name, calling_player.ship.firing_rate,
                calling_player.ship.repairs_available, calling_player.ship.ammo]})

        # send these messages to all players when they first connect
        calling_player.client.broadcast(map_msg)
        for name, value in self.map.weather_types().items():
            calling_player.client.broadcast(self.io_controller.build_message({'command': 'weather',
                'args': [name, value]}))
        calling_player.client.broadcast(wind_msg)
        calling_player.client.broadcast(player_ship_msg)

        game_ready = False
        if self.ready_players >= 2:
            game_ready = True
            self._send_init(calling_player)

        # Once we receive at least 1 player, start. Don't start again after
        if not self.thread_started and game_ready:
            self.run()
            self.thread_started = True

    def add_player(self, client):
        """ This method is responsible for creating a new client and wrapping it in a Player class """
        player = Player(client)
        self.movement_controller.place_player(player)
        player.add_ship(choice(self.all_ships))
        player.ship.sails = 0.0
        player.is_turning = False
        player.is_repairing = False

        if player not in self.active_players:
            self.active_players.append(player)

    def remove_player(self, client_id):
        """ This is responsible for finding the client with the client id and removing it from our clients list """
        to_remove = None
        for p in self.active_players:
            if p.id == client_id:
                to_remove = p
        if to_remove:
            self.surrender_player(to_remove)

    def _fire_broadside(self, calling_player, args):
        """ Calculates a broadside attack from the calling_player to its target

            Returns the side that the firing player is firing from """
        try:
            target_player = [p for p in self.active_players if str(p.id) == args[0]][0]
        except IndexError:
            return

        # side[0] is the true/false and side[1] is the side fired from
        side = self.attack_controller.fire_broadside(calling_player, target_player)
        if not side[1] and side[0] == 'R':
            # Ship wasn't in range
            return

        if target_player.player_state == PlayerStatus.SUNK:
            all_scores = Scores.query.all()
            player_field = [p for p in all_scores if target_player.name == p.player_name][0]
            elixir.session.begin()
            player_field.losses += 1
            elixir.session.commit()
            self.surrender_player(target_player)

        self.send_to_all(self.io_controller.build_message({'command': 'shipStatus',
            'args': [target_player.id, target_player.ship.hit_points / target_player.ship.max_hit_points, target_player.player_state]}))

        self.send_to_all(self.io_controller.build_message({'command': 'cannonsFired',
            'args': [calling_player.id, side[0]]}))

    def _change_speed(self, calling_player, args):
        """ Changes the speed of the calling_player ship and sends the new speed back to the client """
        self.movement_controller.set_sails(calling_player, args[0])
        self.send_to_all(self.io_controller.build_message({'command': 'setSpeed',
            'args': [calling_player.id, calling_player.ship.sails]}))

    def _change_heading(self, calling_player, args):
        """ Changes the heading of the calling_player and sends the new heading back to the client """
        self.movement_controller.change_heading(calling_player, int(args[0]))
        self.send_to_all(self.io_controller.build_message({'command': 'setHeading',
            'args': [calling_player.id, calling_player.requested_heading]}))

    def _game_surrender(self, calling_player, args):
        """ Surrenders the calling_player and sending the ship status back to the client """
        self.surrender_player(calling_player)
        all_scores = Scores.query.all()
        player_field = [p for p in all_scores if calling_player.name == p.player_name][0]
        elixir.session.begin()
        player_field.surrenders += 1
        elixir.session.commit()

        self.send_to_all(self.io_controller.build_message({'command': 'shipStatus',
            'args': [calling_player.id, 0.0, 5]}))

    def _repair(self, calling_player, args):
        result = self.attack_controller.repair_ship(calling_player)
        damage_ratio = calling_player.ship.hit_points / calling_player.ship.max_hit_points

        calling_player.is_repairing = True
        threading.Timer(result[1], self.stop_repairing, (calling_player,)).start()

        self.send_to_all(self.io_controller.build_message({'command': 'shipStatus',
            'args': [calling_player.id, damage_ratio, calling_player.player_state]}))

        self.send_to_all(self.io_controller.build_message({'command': 'repair',
            'args': [calling_player.id, int(result[0])]}))

    def surrender_player(self, player):
        """ Removes the player from the global active players list """
        try:
            msg = self.io_controller.build_message({'command': 'setSpeed', 'args': [player.id, 0.0]})
        except AttributeError:
            return
        self.send_to_all(msg)
        time.sleep(self.update_timeout + 0.1)
        self.inactive_players.append(player)
        try:
            self.active_players.remove(player)
        except ValueError:
            # Couldn't remove for some reason
            pass

    def player_sunk(self, player):
        """ When a player sinks, they lose """
        all_scores = Scores.query.all()
        player_field = [p for p in all_scores if player.name == p.player_name][0]
        elixir.session.begin()
        player_field.losses += 1
        elixir.session.commit()
        self.surrender_player(player)

    def victor(self):
        """ Checks if there exists 1 active player """
        winner = len(self.active_players) == 1
        if winner and not self.gameFinished:
            self.gameFinished = True
            all_scores = Scores.query.all()
            player_field = [p for p in all_scores if self.active_players[0].name == p.player_name][0]
            elixir.session.begin()
            player_field.wins += 1
            elixir.session.commit()
        return winner

    def send_to_all(self, message):
        for p in self.active_players + self.inactive_players:
            p.client.broadcast(message)
