""" This is the module for Movement Controller Class """
import math
import random

from src.player import PlayerStatus

class MovementController(object):
    """ This class is used to encapsulate all movement related activities """
    def __init__(self, map):
        self.TURN_RADIUS_FACTOR = 5
        self.map = map
        self.map_x = map.x
        self.map_y = map.y
        self.last_x = self.map_x / 2
        self.last_y = self.map_y

    def update_position(self, player, direction=0, time_intval=1, active_players=None):
        """ Updates the player position based on a straight line """
        speed = self.calculate_ship_speed(player, self.map.wind_speed, self.map.wind_dir)

        player.position[0] += math.sin(math.radians(direction)) * speed * time_intval
        player.position[1] -= math.cos(math.radians(direction)) * speed * time_intval

        self.check_boundaries(player)

        for p in active_players:
            if player.id == p.id:
                continue

            hit = self.check_collision(player, p)
            if hit:
                p.player_state = PlayerStatus.SUNK
                player.player_state = PlayerStatus.SUNK

    def check_collision(self, player1, player2):
        """Checks if two boats are within range of one another """

        xdist = abs(player1.position[0] - player2.position[0])
        ydist = abs(player1.position[1] - player2.position[1])
        distance = math.sqrt((xdist * xdist) + (ydist * ydist))
        return distance <= 50

    def place_player(self, player):
        """ Places each player randomly on map. This is used when we initially spawn ships """
        player.position = [random.randrange(0, self.map_x, 50), random.randrange(0, self.map_y, 50)]

    def calculate_ship_speed(self, player, wind_speed, wind_direction):
        """ Calculates the ship speed, converting to positive number if neccessary """

        theta = (player.heading * math.pi / 180.0) - (wind_direction * math.pi / 180.0)
        if theta < 0:
            theta += math.pi * 2.0
        alpha = player.ship.max_angle_in_rads() - math.pi / 2.0

        if math.pi / 2.0 >= theta >= 0 or 2 * math.pi >= theta >= 3.0 * math.pi / 2.0:
            speed = player.ship.sails * ((player.ship.max_ratio * wind_speed - wind_speed) *
                    math.fabs(math.sin(theta)) + wind_speed)
        elif math.pi / 2.0 + alpha >= theta > math.pi / 2.0:
            speed = player.ship.sails * (0.5 * (player.ship.max_ratio * wind_speed *
                    math.cos((math.pi / alpha) * (theta - (math.pi / 2.0))) +
                    player.ship.max_ratio * wind_speed))
        elif 3.0 * math.pi / 2.0 > theta >= 3.0 * math.pi / 2.0 - alpha:
            speed = player.ship.sails * (0.5 * (player.ship.max_ratio * wind_speed *
                    math.cos((math.pi / alpha) * (theta - (3.0 * math.pi / 2.0 + 2.0 * alpha))) +
                    player.ship.max_ratio * wind_speed))
        else:
            speed = 0

        return speed

    def update_turning(self, player, direction=0):
        """ Updates the players heading based on their direction """
        player.is_turning = True
        # split the turn into equal-ish parts
        theta = math.radians(direction)
        turn_radius = self.turn_radius(player)
        side_length = math.sqrt((2 * (turn_radius ** 2)) - ((2 *( turn_radius ** 2)) * (math.cos(theta))))

        alpha = (math.pi - theta) / 2.0 - math.radians(player.heading)
        player.position[0] += side_length * math.cos(alpha)
        player.position[1] -= side_length * math.sin(alpha)

        self.check_boundaries(player)

        player.heading += direction
        if player.heading > 360:
            player.heading %= 360
        elif player.heading < 0:
            player.heading += 360

        time_intval = theta / player.ship.angular_velocity(self.TURN_RADIUS_FACTOR)
        player.requested_heading = 0

        return math.fabs(time_intval)

    def change_heading(self, player, direction):
        """ Changes the heading of a player given a degree (-180 - 180) """
        if 180 >= direction >= -180:
            player.requested_heading = direction

    def set_sails(self, player, sails):
        """ Sets the sail ratio between 0.0 and 1.0 """
        if 0.0 <= float(sails) <= 1.0:
            player.ship.sails = float(sails)

    def turn_radius(self, player):
        """ Calculate the turn radius based on the players speed and angular velocity """
	speed = self.calculate_ship_speed(player, self.map.wind_speed, self.map.wind_dir)

        return speed / float(player.ship.angular_velocity(self.TURN_RADIUS_FACTOR))
        #return player.ship.sails / float(player.ship.angular_velocity(player.ship.turn_radius_factor))

    def check_boundaries(self, player):
        if (0 < player.position[0] < self.map_x) and (0 < player.position[1] < self.map_y): return
        else:
            player.ship_speed = 0
            if player.position[0] < 0:  player.position[0] = 0
            elif player.position[0] > self.map_x:   player.position[0] = self.map_x
            elif player.position[1] < 0:    player.position[1] = 0
            elif player.position[1] > self.map_y:   player.position[1] = self.map_y
