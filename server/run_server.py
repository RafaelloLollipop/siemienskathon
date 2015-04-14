import pika
from multiprocessing.managers import BaseManager
from subprocess import Popen
import subprocess
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import sys
import os
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
        #create sharedmemory
        current_path = os.path.dirname(os.path.abspath(__file__))
        #server = subprocess.Popen([sys.executable, os.path.join(current_path, 'handler', 'handler_memory.py')])  # something long running
        address = "127.0.0.1"
        print("Create server object")
        server = subprocess.Popen([sys.executable, os.path.join(current_path, 'core', 'server.py')])  # something long running
        # ... do other stuff while subprocess is running)
        port = 8888
        http_server = tornado.httpserver.HTTPServer(application)
        print("Listening on {0}:{1}".format(address, port))
        http_server.listen(address=address, port=port)
        tornado.ioloop.IOLoop.instance().add_timeout(timedelta(seconds=3),
                                                 send_message_to_clients)
        tornado.ioloop.IOLoop.instance().start()
        server.terminate()