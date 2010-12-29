import math
import unittest

from src.models import Ship, ShipType

class ShipTester(unittest.TestCase):
    def setUp(self):
        self.ship = Ship(name=u"Test", hit_points=100, max_speed=10, num_cannons=50,
                ship_type=u"TEST", turn_radius_factor=2.0, max_ratio=1.0,
                max_theta=180, sails=0.0)

    def test_creation(self):
        """ Test that we can create a ship, initialize it with values and retrieve those values """
        # test that various values were set
        self.assertEquals(self.ship.name, u"Test")
        self.assertEquals(self.ship.num_cannons, 50)
        self.assertEquals(self.ship.max_theta, 180)

    def test_broadside_damage(self):
        """ Tests that the broadside damage is calculated correctly
            It should be ceil(num_cannons/2) """
        self.assertEquals(self.ship.broadside_damage(),
                math.ceil(self.ship.num_cannons / 2))

    def test_take_damage(self):
        """ Tests that a ship can take damage and that the HP is subtracted accordingly """
        self.assertEquals(self.ship.hit_points, 100)
        self.ship.take_damage(5)
        self.assertEquals(self.ship.hit_points, 95)

if __name__ == '__main__':
    suit = unittest.TestLoader().loadTestsFromTestCase(ShipTester)
    unittest.TextTestRunner(verbosity=3).run(suit)
