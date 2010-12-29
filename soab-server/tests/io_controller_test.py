import unittest

from src.io_controller import IOController

class IOControllerTest(unittest.TestCase):
    def setUp(self):
        self.io = IOController()

    # parsing command with 2 args
    def test_MapCommand(self):
        """ Tests parsing the mapSize command part of the message """
        test = 'mapSize 1000 1000'
        output = self.io.parse_message(test)
        self.assertEquals(output['command'], 'mapSize')

    # parsing >1 args
    def test_MapDimension(self):
        """ Tests parsing the mapSize arguments part of the message """
        test = 'mapSize 1000 1000'
        output = self.io.parse_message(test)
        self.assertEquals(output['args'], ['1000','1000'])

    # parsing command with 1 args
    def test_AttackCommand(self):
        """ Tests parsing the fireBroadsize command part of the message """
        test = 'fireBroadside 3'
        output = self.io.parse_message(test)
        self.assertEquals(output['command'], 'fireBroadside')

    # parsing 1 args
    def test_AttackArgs(self):
        """ Tests parsing the fireBroadside arguments part of the message """
        test = 'fireBroadside 3'
        output = self.io.parse_message(test)
        self.assertEquals(output['args'], ['3'])

    # parsing dict -> string conversion
    def test_cannonsCommand(self):
        """ Tests parsing the cannonsFired command string into a client message """
        test = {'command': 'cannonsFired','args': ['123', 'P']}
        output = self.io.build_message(test)
        self.assertEquals(output, 'cannonsFired 123 P')

if __name__ == '__main__':
    suit = unittest.TestLoader().loadTestsFromTestCase(IOControllerTest)
    unittest.TextTestRunner(verbosity=3).run(suit)
