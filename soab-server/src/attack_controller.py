import math

from src.player import PlayerStatus

class AttackController(object):

    def fire_cannon(self, p1, p2):
        """ Fires a single cannon; p1 is the firing player, and fires on p2 """
        if self.in_range(p1, p2):   #fire if ships are in range
            result = self.check_hit(p1, p2)
            if result[1]: self.calculate_damage(p2, 1)
            if (p2.hit_points / p2.max_hit_points) <= 0.25:
                p2.player_state = PlayerStatus.ON_FIRE
            return result[0]

        else:   return False

    def fire_broadside(self, p1, p2):
        """ Fires a broadside; player p1 fires on player p2 """
        if self.in_range(p1, p2):   # fire if ships are in range
            result = self.check_hit(p1, p2)
            if result[1]: self.calculate_damage(p2, p1.ship.broadside_damage())
            self.check_ship_status(p2)
            return result

        else:   return ('R', False)

    def in_range(self, p1, p2):
        """ Determines if two players are within firing range of each other """

        # calculate horizontal and vertical distances between ships
        xdist = abs(p1.position[0] - p2.position[0])
        ydist = abs(p1.position[1] - p2.position[1])
        distance = math.sqrt((xdist * xdist) + (ydist * ydist)) # calculate true distance between ships
        return distance <= p1.ship.firing_range

    def calculate_damage(self, player, damage):
        """ Calculates the damage done to a player, and updates player hitpoints """

        # update hitpoints and maximum speed for player
        player.ship.take_damage(damage)
        self.update_max_speed(player, damage)
        if player.ship_speed > player.ship.max_speed:   player.ship_speed = player.ship.max_speed

    def alive(self, player):
        """ Used to determine if a player has been destroyed """

        return player.ship.hit_points > 0

    def surrender(self, player):
        """" player requests surrender """

        player.ship.hit_points = 0

    def update_max_speed(self, player, damage):
        """ Updates the maximum ship speed of player based on damage received """

        player.ship.max_speed = player.ship.max_speed - damage
        if player.ship.max_speed < 0:  player.ship.max_speed = 0 # speed can't be less than 0

    def check_hit(self, p1, p2):
        """ Checks to see if p1 can hit enemy ship based on relative angle """

        xdist = p2.position[0] - p1.position[0]
        ydist = p1.position[1] - p2.position[1]

        rel_angle = self.arctan(ydist, xdist)
        if rel_angle > 180: rel_angle -= 360

        angle_diff = p1.heading - rel_angle

        if angle_diff > 180:    angle_diff -= 360
        elif angle_diff < -180: angle_diff += 360

        diff = math.fabs(angle_diff)
        if (60 <= diff) and (diff <= 120):
            if angle_diff < 0: return ('S', True)
            else:   return ('P', True)

        else:
            if angle_diff < 0: return ('S', False)
            else:   return ('P', False)

    def has_ammo(self, player):
        """ Checks if a ship has ammunition """
        return player.ship.ammo > 0

    def update_ammo(self, player, ammo_fired):
        """ Update ammunition levels on a ship """
        player.ship.reduce_ammo(ammo_fired)

    def arctan(self, y, x):
        """ Arctan function that returns an angle between -180 and 180 """
        return (math.degrees(math.atan2(y, x)) * (-1)) + 90

    def repair_ship(self, player):
        """ Repairs a ship """
        if player.ship.repairs_available <= 0:
            return (False, 0)
        if player.ship.full_health():   return (False, 0)
        healing = player.ship.max_hit_points * 0.3
        time = healing / player.ship.repair_rate
        player.ship.heal_damage(healing)
        player.player_status = PlayerStatus.PLAYING
        player.ship.repairs_available -= 1
        return (True, time)

    def check_ship_status(self, player):
        """ This calculates the ship status of the player and returns the status """
        damage_ratio = float(player.ship.hit_points / player.ship.max_hit_points)
        if 0.0 <= damage_ratio <= 0.25:
            player.player_state = PlayerStatus.ON_FIRE

        if not self.alive(player):
            player.player_state = PlayerStatus.SUNK
            return False

        return True
