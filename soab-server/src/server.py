from twisted.application import service
from twisted.internet import protocol
from twisted.protocols import basic
from twisted.python import log
from twisted.web import http

from websocket import WebSocketHandler

from game import Game
from models import *

#class Server(basic.LineReceiver):
class Server(WebSocketHandler):
    """ This server implements the Twisted line receiver server """

    delimiter = "\n"

    def __init__(self):
        print dir(self)

    def connectionMade(self):
        """ Checks if we already have that client, if not, adds them to our list """
        if self not in self.factory.clients:
            self.id = self.transport.getPeer().port
            log.msg("Client", self.id, "connected")
            self.factory.clients.append(self)
            self.factory.game.add_player(self)

    def connectionLost(self, reason):
        """ When a client disconnects, remove them from all lists """
        log.msg("Lost client", self.id)
        self.factory.clients.remove(self)
        self.factory.game.remove_player(self.id)

    def lineReceived(self, line):
        print repr(line)

    def frameReceived(self, frame):
        print "IN HERE!!!"
        """ When we receive a line from the client, send it to our game """
        log.msg("Received:", repr(frame), "from client", self.id)
        self.factory.game.send_message(self, frame)

    def broadcast(self, message):
        """ Send a message to the client """
        try:
            self.transport.write(message + "\n")
            log.msg("Sending", message, "to client", self.id)
        except TypeError:
            # When we return None from the game class
            # We don't want the message to be written
            pass

class MyServerFactory(protocol.ServerFactory):
    """ This factory creates some instances variables that are accessible in our Server """
    protocol = Server

    def __init__(self, service):
        self.service = service
        self.clients = []
        self.game = Game(self.service.map, self.service.max_players)

class ServerService(service.Service):
    """ This service runs the server and starts the service so our server can be run like a service """
    def __init__(self, map, max_players):
        self.map = map
        self.max_players = max_players

    def startService(self):
        service.Service.startService(self)
        log.msg("Created Game on map", self.map, "with", self.max_players, "max players")
