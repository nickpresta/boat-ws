
""" This is a unit test for the AttackController class. The suite tests all methods to ensure functionality"""
""" Created by Michael Delong for Snakes On a Boat server """

import unittest
import math

from src.attack_controller import AttackController

class ShipDummy(object):
    """ Dummy Ship class with necessary methods and variables used for test cases """
    
    def __init__(self, ncannons):
        self.hit_points = 100
        self.num_cannons = ncannons
        self.max_speed = 100

    def take_damage(self, damage):
        self.hit_points = self.hit_points - damage
        if self.hit_points < 0: self.hit_points = 0

    def broadside_damage(self):
        return math.ceil(self.num_cannons/2)

class PlayerDummy(object):
    """ Dummy Player class with necessary methods and variables used for test cases """

    def __init__(self, ncannons, position):
        self.ship = ShipDummy(ncannons)
        self.update_position(position)
        
    def update_position(self, position):
        self.position = (position[0], position[1])

class AttackControllerTester(unittest.TestCase):
    def setUp(self):
        """ Creates an AttackController instance and dummy Player objects to test it with """
        
        self.attack = AttackController()
        l1 = (10, 10)
        l2 = (20, 20)
        self.p1 = PlayerDummy(20, l1) # create sample players
        self.p2 = PlayerDummy(10, l2)
    
    def test_inRange(self):
        """ Testing that in_range() reports correct values for ships in and out of firing range """
        
        self.p1.update_position((10, 10)) # test for the case when ships are in range
        self.p2.update_position((20, 20))
        result = self.attack.in_range(self.p1, self.p2)
        self.assertEquals(result, True) # should return true if in range

        self.p1.update_position((10, 10)) # test for the case when ships are out of range
        self.p2.update_position((800, 800))
        result = self.attack.in_range(self.p1, self.p2)
        self.assertEquals(result, False) # should return false if out of range

    def test_fireCannon(self):
        """ Testing that damage is calculated and updated properly: fire_cannon() """
    
        hp1 = self.p1.ship.hit_points, self.p1.ship.max_speed # get hitpoints prior to calling the method for comparison
        hp2 = self.p2.ship.hit_points, self.p2.ship.max_speed
        
        self.p1.update_position((20, 20))
        self.p2.update_position((10, 10))
        output = self.attack.fire_cannon(self.p1, self.p2)     # run method; p1 fires on p2
        self.assertEquals(output, "P")                        # ships were in range, should have returned port
        self.assertEquals(hp1[0], self.p1.ship.hit_points)     # p1's hp should be unchanged
        self.assertEquals(hp2[0] - 1, self.p2.ship.hit_points) # p2's hp should be reduced by 1
        self.assertEquals(hp1[1], self.p1.ship.max_speed)      # same expectation as with the hp
        self.assertEquals(hp2[1] - 1, self.p2.ship.max_speed)

        hp1 = self.p1.ship.hit_points, self.p1.ship.max_speed
        hp2 = self.p2.ship.hit_points, self.p2.ship.max_speed
        output = self.attack.fire_cannon(self.p2, self.p1) # run method; p2 fires on p1
        # everything should be the same as the previous case, except p1's HP should be reduced instead of p2
        self.assertEquals(output, "S") # output should be starboard
        self.assertEquals(hp2[0], self.p2.ship.hit_points)
        self.assertEquals(hp1[0] - 1, self.p1.ship.hit_points)
        self.assertEquals(hp2[1], self.p2.ship.max_speed)
        self.assertEquals(hp1[1] - 1, self.p1.ship.max_speed)
        
        # test for the cases when both ships are out of range; the firing should fail
        # both ship's HP should remain unchanged
        self.p1.update_position((5, 5))
        self.p2.update_position((800, 800))

        hp1 = self.p1.ship.hit_points, self.p1.ship.max_speed
        hp2 = self.p2.ship.hit_points, self.p2.ship.max_speed
        output = self.attack.fire_cannon(self.p1, self.p2)
        self.assertEquals(output, False)
        self.assertEquals(hp1[0], self.p1.ship.hit_points)
        self.assertEquals(hp2[0], self.p2.ship.hit_points)
        self.assertEquals(hp1[1], self.p1.ship.max_speed)
        self.assertEquals(hp2[1], self.p2.ship.max_speed)

        hp1 = self.p1.ship.hit_points, self.p1.ship.max_speed
        hp2 = self.p2.ship.hit_points, self.p2.ship.max_speed
        output = self.attack.fire_cannon(self.p1, self.p2)
        self.assertEquals(output, False)
        self.assertEquals(hp1[0], self.p1.ship.hit_points)
        self.assertEquals(hp2[0], self.p2.ship.hit_points)
        self.assertEquals(hp1[1], self.p1.ship.max_speed)
        self.assertEquals(hp2[1], self.p2.ship.max_speed)

    def test_fireBroadside(self):
        """ Testing that damage is calculated and updated properly: fire_broadside() """
    
        hp1 = self.p1.ship.hit_points, self.p1.ship.max_speed
        hp2 = self.p2.ship.hit_points, self.p2.ship.max_speed
        self.p1.update_position((10, 10))
        self.p2.update_position((20, 20))
        output = self.attack.fire_broadside(self.p1, self.p2) # run method; p1 fires on p2
        self.assertEquals(output, "S")  # should return starboard; ship was hit
        
        self.assertEquals(hp1[0], self.p1.ship.hit_points) # p1s HP and speed should be unchanged
        self.assertEquals(hp1[1], self.p1.ship.max_speed)
        self.assertEquals(hp2[0] - self.p1.ship.broadside_damage(), self.p2.ship.hit_points) # p2's HP, speed should be reduced appropriately
        self.assertEquals(hp2[1] - self.p1.ship.broadside_damage(), self.p2.ship.max_speed)
        
        # same case as above, except p2 fires on p1
        hp1 = self.p1.ship.hit_points, self.p1.ship.max_speed
        hp2 = self.p2.ship.hit_points, self.p2.ship.max_speed
        output = self.attack.fire_broadside(self.p2, self.p1)
        self.assertEquals(output, "P")
        self.assertEquals(hp2[0], self.p2.ship.hit_points)
        self.assertEquals(hp1[0] - self.p2.ship.broadside_damage(), self.p1.ship.hit_points)
        self.assertEquals(hp2[1], self.p2.ship.max_speed)
        self.assertEquals(hp1[1] - self.p2.ship.broadside_damage(), self.p1.ship.max_speed)
        
        # remaining cases are for ships out of firing range
        # ships should be unable to fire, and HP should remain the same
        self.p1.update_position((5, 5))
        self.p2.update_position((800, 800))

        hp1 = self.p1.ship.hit_points, self.p1.ship.max_speed
        hp2 = self.p2.ship.hit_points, self.p2.ship.max_speed
        output = self.attack.fire_broadside(self.p1, self.p2)
        self.assertEquals(output, False)
        self.assertEquals(hp1[0], self.p1.ship.hit_points)
        self.assertEquals(hp2[0], self.p2.ship.hit_points)
        self.assertEquals(hp1[1], self.p1.ship.max_speed)
        self.assertEquals(hp2[1], self.p2.ship.max_speed)

        hp1 = self.p1.ship.hit_points, self.p1.ship.max_speed
        hp2 = self.p2.ship.hit_points, self.p2.ship.max_speed
        output = self.attack.fire_broadside(self.p1, self.p2)
        self.assertEquals(output, False)
        self.assertEquals(hp1[0], self.p1.ship.hit_points)
        self.assertEquals(hp2[0], self.p2.ship.hit_points)
        self.assertEquals(hp1[1], self.p1.ship.max_speed)
        self.assertEquals(hp2[1], self.p2.ship.max_speed)
    
    def test_calculateDamage(self):
        """ Testing that damage is calculated and updated correctly: calculate_damage() """
    
        hp1 = self.p1.ship.hit_points, self.p1.ship.max_speed
        hp2 = self.p2.ship.hit_points, self.p2.ship.max_speed
        self.attack.calculate_damage(self.p1, 10) # simulate taking 10 points of damage
        self.attack.calculate_damage(self.p2, 5)  # simulate taking 5 points of damage
        
        # make sure damage and max speed for both players are reduced by 10 and 5 respectively
        self.assertEquals(hp1[0] - 10, self.p1.ship.hit_points)
        self.assertEquals(hp2[0] - 5, self.p2.ship.hit_points)
        self.assertEquals(hp1[1] - 10, self.p1.ship.max_speed)
        self.assertEquals(hp2[1] - 5, self.p2.ship.max_speed)
    
    def test_alive(self):
        """ Testing that the alive() method reports ship status correctly for ships that are destroyed and alive """

        self.p1.ship.hit_points = 0 # set hp for both ships to 0, then ensure alive() returns false
        self.p2.ship.hit_points = 0
        self.assertEquals(self.attack.alive(self.p1), False)
        self.assertEquals(self.attack.alive(self.p2), False)
        self.p1.ship.hit_points = 100
        self.p2.ship.hit_points = 100 # test for the case when the ship has not been destroyed
        self.assertEquals(self.attack.alive(self.p1), True) # alive() should return true
        self.assertEquals(self.attack.alive(self.p2), True)
    
    def test_surrender(self):
        """ Testing that the surrender() method works for two different ships """
        
        self.attack.surrender(self.p1)
        self.attack.surrender(self.p2)
        self.assertEquals(self.p1.ship.hit_points, 0)
        self.assertEquals(self.p2.ship.hit_points, 0)
        self.p1.ship.hit_points = 100
        self.p2.ship.hit_points = 100
    
    def test_updateMaxSpeed(self):
        """ Testing that maximum speed of ships is reduced appropriately: update_max_speed() """
        
        hp1 = self.p1.ship.max_speed # get current max speeds for comparison
        hp2 = self.p2.ship.max_speed        
        self.attack.update_max_speed(self.p1, 10) # test method with sample damages
        self.attack.update_max_speed(self.p2, 5)
        self.assertEquals(self.p1.ship.max_speed, hp1 - 10) # player's max speed should be reduced by corresponding amount
        self.assertEquals(self.p2.ship.max_speed, hp2 - 5)

        self.attack.update_max_speed(self.p1, 1000) # test case where max_speed would go below 0
        self.attack.update_max_speed(self.p2, 1000)
        self.assertEquals(self.p1.ship.max_speed, 0) # speed should be 0; cannot be negative
        self.assertEquals(self.p2.ship.max_speed, 0)

if __name__ == '__main__': # load and run test suites
    suite = unittest.TestLoader().loadTestsFromTestCase(AttackControllerTester)
    unittest.TextTestRunner(verbosity=2).run(suite)
