import unittest

from src.models import Map

class MapTest(unittest.TestCase):
    def setUp(self):
        self.map = Map(name=u"Test", x=1000, y=1000, wind_speed=50, wind_dir=250)

    def test_creation(self):
        """ Test that we can create a map, initialize it with values and retrieve those values """
        # test that various values were set
        self.assertEquals(self.map.name, u"Test")
        self.assertEquals(self.map.wind_speed, 50)
        self.assertEquals(self.map.wind_dir, 250)
        self.assertEquals(self.map.x, 1000)
        self.assertEquals(self.map.y, 1000)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MapTest)
    unittest.TextTestRunner(verbosity=3).run(suite)
