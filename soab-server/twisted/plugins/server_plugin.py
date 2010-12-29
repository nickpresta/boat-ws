from zope.interface import implements
from twisted.application import service
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application.internet import TCPServer

import settings
from src.server import *

class Options(usage.Options):
    optParameters = [["port", "p", settings.PORT, "The port the server runs on"],
                     ["map", "m", None, "The map to play on."],
                     ["numplayers", "n", 4, "The maximum number of players"]]

class ServerServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "soabserver"
    description = "Snakes on a Boat Server"
    options = Options

    def makeService(self, options):
        top_service = service.MultiService()

        server_service = ServerService(options["map"], int(options["numplayers"]))
        server_service.setServiceParent(top_service)

        server_factory = MyServerFactory(server_service)

        server = TCPServer(int(options["port"]), server_factory)
        server.setServiceParent(top_service)

        return top_service

service_Maker = ServerServiceMaker()
