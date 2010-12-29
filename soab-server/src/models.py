""" This is the module with all our model definitions """

import math

import elixir

import settings

elixir.metadata.bind = settings.DATABASE

class ShipType(object):
    """ This class is used as an ENUM type to represent our ship types """
    CORVETTE = u"Corvette"
    GALLEON = u"Galleon"
    FRIGATE = u"Frigate"
    BRIG = u"Brig"
    MERCHANT = u"Merchant"
    PRIVATEER = u"Privateer"
    GUNBOAT = u"Gunboat"
    MAN_OF_WAR = u"Man-of-War"

class ShipState(object):
    """ This class is used as an ENUM type to represent our ship state """
    NORMAL = 0
    SUNK = 1
    GROUNDED = 2
    ON_FIRE = 3
    A_DRIFT = 4
    SURRENDERED = 5

class Ship(elixir.Entity):
    """ This represents our ship and all the fields it needs to store our data """
    elixir.using_options(tablename="soab_ship")

    hit_points = elixir.Field(elixir.Integer)
    max_hit_points = elixir.Field(elixir.Integer)
    max_speed = elixir.Field(elixir.Integer)
    num_cannons = elixir.Field(elixir.Integer)
    ship_type = elixir.Field(elixir.UnicodeText) # From our ShipType
    name = elixir.Field(elixir.UnicodeText)
    turn_radius_factor = elixir.Field(elixir.Float)
    max_ratio = elixir.Field(elixir.Float)
    max_theta = elixir.Field(elixir.Integer)
    sails = elixir.Field(elixir.Float)
    ammo = elixir.Field(elixir.Integer)
    firing_range = elixir.Field(elixir.Integer)
    firing_rate = elixir.Field(elixir.Float)
    repair_rate = elixir.Field(elixir.Float)
    repairs_available = elixir.Field(elixir.Integer)

    state = ShipState.NORMAL

    def max_angle_in_rads(self):
        return math.radians(self.max_theta)

    def angular_velocity(self, turn_factor):
        return 1 / (turn_factor * self.turn_radius_factor)

    def hp_as_percent(self):
        return math.ceil(self.hit_points / self.max_hit_points)

    def broadside_damage(self):
        return math.ceil(self.num_cannons / 2)

    def heal_damage(self, hit_points):
        self.hit_points += hit_points
        if self.hit_points > self.max_hit_points:
            self.hit_points = self.max_hit_points

    def take_damage(self, damage):
        self.hit_points -= damage
        if self.hit_points < 0:
            self.hit_points = 0

    def reduce_ammo(self, ammo_fired):
        self.ammo -= ammo_fired
        if self.ammo < 0:
            self.ammo = 0

    def full_health(self):
        return self.hit_points == self.max_hit_points

    def has_ammo(self):
        return self.ammo > 0

    def __repr__(self):
        return '<Ship "%s" (hp=%d, max_speed=%d, num_cannons=%d, type=%s, firing_rate=%d)>' % (self.name,
                self.hit_points, self.max_speed, self.num_cannons, self.ship_type, self.firing_rate)

class Map(elixir.Entity):
    """ This represents our map and all the data it needs """
    elixir.using_options(tablename="soab_map")

    name = elixir.Field(elixir.UnicodeText)
    x = elixir.Field(elixir.Integer)
    y = elixir.Field(elixir.Integer)
    wind_speed = elixir.Field(elixir.Integer)
    wind_dir = elixir.Field(elixir.Integer)
    rain = elixir.Field(elixir.Float)
    fog = elixir.Field(elixir.Integer)
    waves = elixir.Field(elixir.Float)

    def weather_types(self):
        """ Returns all the fields that make up the weather """
        return {'rain': self.rain, 'fog': self.fog, 'waves': self.waves}

    def __repr__(self):
        return '<Map "%s" (x=%d, y=%d, wind_speed=%d, wind_dir=%d)>' % (self.name,
                self.x, self.y, self.wind_speed, self.wind_dir)

class Scores(elixir.Entity):
    """ This class is a high score table for our game. Keeps track of wins, surrenders, and loses """
    elixir.using_options(tablename='soab_scores')

    player_name = elixir.Field(elixir.UnicodeText)
    wins = elixir.Field(elixir.Integer)
    losses = elixir.Field(elixir.Integer)
    surrenders = elixir.Field(elixir.Integer)

    def total_games(self):
        """ Calculates the total games played for a specific player """
        return self.wins + self.surrenders + self.losses

    def score(self):
        """ Creates a score based on the number of wins, loses, and surrenders """
        return (3 * self.wins) + (1 * self.surrenders) + (-1 * self.losses)

elixir.setup_all()
