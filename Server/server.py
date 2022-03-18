from http.server import HTTPServer
from Logger import logger
from Server import RequestHandler
from Config import config


def server():
    NAME = config.Server.name
    VERSION = config.Server.version
    DEBUG = config.Debug.open
    LOCAL_HOST = config.Server.local_host
    SERVER_HOST = config.Server.server_host
    PORT = config.Server.port
    if DEBUG:
        name = LOCAL_HOST
    else:
        name = SERVER_HOST
    port = PORT
    host = LOCAL_HOST
    serverAddress = (host, port)
    logger.info("{}-{}".format(NAME, VERSION))
    logger.info("http://{}:{}/".format(name, port))
    httpServer = HTTPServer(serverAddress, RequestHandler)
    httpServer.serve_forever()
