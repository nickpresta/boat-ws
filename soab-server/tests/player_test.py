import unittest

from src.player import Player

class PlayerTest(unittest.TestCase):
    def setUp(self):
        # no client object is needed for this example
        self.player = Player(None)

if __name__ == '__main__':
    suit = unittest.TestLoader().loadTestsFromTestCase(PlayerTest)
    unittest.TextTestRunner(verbosity=3).run(suit)
