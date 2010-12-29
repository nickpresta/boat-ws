""" This is the module for our IO controller class """
class IOController(object):
    def parse_message(self, message):
        """ This method parses a plain text message and converts it to a dictionary """
        parts = message.split()
        command = parts[0]
        args = parts[1:]

        out = {'command': command, 'args': args}

        return out

    def build_message(self, message):
        """ This creates a single string to send back to the client """
        # Make sure all args are strings
        message['args'] = [str(i) for i in message['args']]
        return "{0} {1}".format(message['command'], ' '.join(message['args']))
