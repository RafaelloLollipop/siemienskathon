import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import sys
import getopt
import json
import jsonpickle
from Room import Room
from Games.Game import Game
from Server import Server
from Player import Player


class ClientHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print('new connection')
        #self.write_message("Hello World")

    def on_message(self, message):
        print(self.request.remote_ip)
        print(message)
        response = self.handle_request(message)
        resp = json.dumps(response)
        print("Send response:")
        print(resp)
        self.write_message(resp)

    def handle_request(self, data):
        response = {'message': "NOPE_OK"}
        data = json.loads(data)
        if data['message'] == 'connectToServer':
            #player_name = data['message']['player_name']
            player_name = "test"
            self.player = Player(self, player_name)
            response = self.get_rooms_list_info()
            return response

        if data['message'] == 'connectToRoom':
            room_id = data['data']['room_id']
            #room_id = 1
            server = Server.get_from_memcached()
            room = server.get_room_by_id(room_id)
            room.add_player(self.player)
            Server.save_to_memcached(server)
            #game_name = room.game.name
            game_name = "demo"
            game_script = "http://" + self.request.host + "/games/" + game_name + "/js/game.js"
            print(game_script)
            response = {'message': "roomUpdate",
                        'data': {
                            'players': [],
                            'game': game_name,
                            'game_script': game_script
                            }
                        }
            return response
        if data['message'] == 'exitRoom':
            response = {'message': "OK",
                        }
            return response
        if data['message'] == 'selectGame':
            response = {'message': "OK",
                        }
            return response
        if data['message'] == 'ready':
            response = {'message': "OK",
                        }
            return response
        if data['message'] == 'newRoom':
            room_name = data['data']['room_name']
            self.create_new_room(room_name)
            response = self.get_rooms_list_info()
            return response
        if data['message'] == 'gameList':
            game_list = ['demo']
            game_list = Game.getGamesArray()
            response = {'message': "gameList",
                        'data': {
                            'game_list': game_list
                            }
                        }
            return response
        return response

    def get_rooms_list_info(self):
        server = serv.get_from_memcached()
        rooms = []
        rooms = server.get_rooms_list()
        ant = [3, 'AntekTworca', 0, 8, 'Labirynt  - zaprszam']
        adam = [1, 'AdamTworca', 5, 8, 'Gramy w mafie, polecam']
        raf = [2, 'RafalTworca', 0, 8, 'sssa']
        rooms.append(ant)
        rooms.append(adam)
        #rooms.append(raf)
        response = {'message': "rooms",
                    'data': {
                        'rooms': rooms
                        }
                    }
        return response

    def create_new_room(self, room_name):
        server = serv.get_from_memcached()
        server.create_room(self.player, room_name)

    def on_close(self):
        print('connection closed')

    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r'/game', ClientHandler),
    (r'/games/(.*)', tornado.web.StaticFileHandler, {'path': './Games/'})
])


if __name__ == "__main__":
    serv = Server()
    Server.save_to_memcached(serv)
    address = ''
    port = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ha:', ['address='])
    except getopt.GetoptError:
        print("-a address")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("HELP")
        if opt == '-a':
            address, port = arg.split(':')
    if not(address and port):
        address = '127.0.0.1'
        port = 8888
    http_server = tornado.httpserver.HTTPServer(application)
    print("Run server on {address}:{port}".format(address=address, port=port))
    http_server.listen(port=port, address=address)
    tornado.ioloop.IOLoop.instance().start()
