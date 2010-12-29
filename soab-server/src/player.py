""" This is the Module for Player Class """
import random

class PlayerStatus(object):
    """ This class is used as an Enum type to identify the status of each player
        in the game """
    DEFEATED = 1
    WON = 0
    SURRENDERED = 5
    PLAYING = 0
    SUNK = 1
    GROUND = 2
    ON_FIRE = 3
    ADRIFT = 4

class Player(object):
    """ This Player class represents the player, the ship the player has, the position,
        player name, etc. Will be expanded to add teams later """

    def __init__(self, client):
        self.client = client
        self.name = "PLAYER"
        self.id = self.client.id
        self.position = [0, 0]
        self.ship_speed = 0
        self.ship = None
        self.heading = random.randrange(-90, 90, 90)
        self.requested_heading = self.heading
        self.player_state = PlayerStatus.PLAYING

    def add_ship(self, ship):
        """ Add a ship to a player """
        self.ship = ship

    def update_state(self, state):
        """ Updates the state of a player """
        self.player_state = state

    def update_position(self, position):
        """ Updates the position of the player given a tuple with x/y coords """
        self.position = position

    def in_bounds(self):
        """ Checks if a player is within bounds """
        pass #check if ship has gone past boundaries of map
