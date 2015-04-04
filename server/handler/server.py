import tornado.websocket
import json
from core.player import Player
from core.server import Server
class ServerHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, handler):
        self.handler = handler

    def on_message(self, message):
        print("Server Handler from {0} recived".format(self.handler.request.remote_ip))
        print(json.dumps(message, indent=4))
        self.handle_request(message)

    def handle_request(self, request):
        response = {'message': "I don't understand you",
                    'data': {}}
        method_name = request['message']
        data = request['data']
        if method_name == "connectToServer":
            self.connect_to_server(data)
        elif method_name == "getRoomsList":
            self.get_rooms_list(data)
        else:
            self.write_response(response)

    def write_response(self, response):
        self.handler.write_message(response)

    def connect_to_server(self, player_name):
        player = Player(self, player_name)
        server = Server.get_from_memcached()
        server.add_player(player)

        response = {'message': "connectSuccess",
                    'data': {
                             'player_id' : player.id
                            }
                    }
        self.write_response(response)

    def get_rooms_list(self, data):
        server = Server.get_from_memcached()
        rooms = []
        rooms = server.get_rooms_list()
        ant = [3, 'AntekTworca', 0, 8, 'Labirynt  - zaprszam']
        adam = [1, 'AdamTworca', 5, 8, 'Gramy w mafie, polecam']
        raf = [2, 'RafalTworca', 0, 8, 'sssa']
        rooms.append(ant)
        rooms.append(adam)
        rooms.append(raf)
        response = {'message': "rooms",
                     'data': {
                         'rooms': rooms
                         }
                     }
        self.write_response(response)