import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import sys
import getopt
import json
import jsonpickle
from game.game import Game
from core.server import Server
from core.player import Player
from handler.client import ClientHandler
from handler.server import ServerHandler
from handler.room import RoomHandler
from handler.connection import ConnectionHandler


application = tornado.web.Application([
    (r'/', ConnectionHandler),
    (r'/games/(.*)', tornado.web.StaticFileHandler, {'path': './Games/'})
])


if __name__ == "__main__":
        address = "127.0.0.1"
        port = 8888
        print("Create server object")
        serv = Server()
        print("Save in memcache")
        Server.save_to_memcached(serv)
        print("Create http server")
        http_server = tornado.httpserver.HTTPServer(application)
        print("Listening on {0}:{1}".format(address, port))
        http_server.listen(address=address, port=port)
        tornado.ioloop.IOLoop.instance().start()