from asyncio import coroutine
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.web import asynchronous
import tornado.websocket
import json
from core.player import Player
from core.server import Server
import time
from multiprocessing.managers import BaseManager
class ListManager(BaseManager): pass
ListManager.register('get_client_list')
m = ListManager(address=('localhost', 50000), authkey=123)


class ServerHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, handler):
        self.handler = handler

    @asynchronous
    def on_message(self, message):
        #print("Server Handler from {0} recived".format(self.handler.request.remote_ip))
        #print(json.dumps(message, indent=4))
        self.handle_request(message)

    @asynchronous
    def handle_request(self, request):
        response = {'message': "I don't understand you",
                    'data': {}}
        method_name = request['message']
        data = request['data']
        if method_name == "connectToServer":
            self.connect_to_server(data)
        elif method_name == "getRoomsList":
            self.get_rooms_list()
        elif method_name == "createNewRoom":
            self.create_new_room(data)
        else:
            self.write_response(response)

    def write_response(self, response):
        print(response)
        self.handler.write_message(response)


    @asynchronous
    def connect_to_server(self, player_name):
        player_id = self.add_new_user(player_name, callback=self.write_response)
        # response = {'message': "connectSuccess",
        #             'data': {
        #                      'player_id' : player_id
        #                     }
        #             }
        # self.write_response(response)

    @gen.coroutine
    @asynchronous
    def add_new_user(self, player_name, callback):
        #m.connect()
        #player = Player(self, player_name)
        #user_list = m.get_client_list()
        #new_user = Player(self, "Vacek")
        #user_list.append(new_user)
        #user_list.append("XD")
        #player_id = new_user.id

        callback(response)


    def get_rooms_list(self):
        server = Server.get_from_memcached()
        rooms = []
        rooms = server.get_rooms_list()
        ant = [3, 'AntekTworca', 0, 8, 'Labirynt  - zaprszam']
        adam = [1, 'AdamTworca', 5, 8, 'Gramy w mafie, polecam']
        raf = [2, 'RafalTworca', 0, 8, 'sssa']
        #rooms.append(ant)
        #rooms.append(adam)
        #rooms.append(raf)
        response = {'message': "rooms",
                     'data': {
                         'rooms': rooms
                         }
                     }
        self.write_response(response)

    def create_new_room(self, data):
        room_name = data['room_name']
        creator_id = data['creator_id']
        server = Server.get_from_memcached()
        server.create_room(creator_id, room_name)
        response = {'message': "createRoomSuccess",
                    'data': {
                             'room_id' : room_name
                            }
                    }
        self.write_response(response)