import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import sys
import getopt
import json
import jsonpickle
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

    def on_close(self):
        server = Server.get_from_memcached()
        server.delete_player(self.player.id)


    def handle_request(self, data):
        response = {'message': "NOPE_OK"}
        data = json.loads(data)
        if data['message'] == 'connectToServer':
            player_name = data['data']['player_name']
            response = self.connectToServer(player_name)
            return response

        if data['message'] == 'connectToRoom':
            room_id = data['data']['room_id']
            server = Server.get_from_memcached()
            if self.player.room_id:
                server.remover_player_from_room(self.player.room_id, self.player.id)
            server.add_player_to_room(room_id, self.player.id)
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
            response = self.all_ready()
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

    def all_ready(self):
        game = Game.getGameByName("Demo")
        server = Server.get_from_memcached()
        gra = game(server.players)
        gra.doAction({'id': server.players[0].id, 'action': 'start'})

    def connectToServer(self, player_name):
        self.player = Player(self, player_name)
        server = Server.get_from_memcached()
        server.add_player(self.player)
        self.send_id_to_player()
        return self.get_rooms_list_info()

    def send_id_to_player(self):
        response = {'message': "connectSuccess",
            'data': {
                    'player_id': self.player.id
                }
            }
        self.write_message(response)

    def get_rooms_list_info(self):
        server = serv.get_from_memcached()
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
        return response

    def create_new_room(self, room_name):
        server = serv.get_from_memcached()
        server.create_room(self.player.id, room_name)


    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r'/game', ClientHandler),
    (r'/games/(.*)', tornado.web.StaticFileHandler, {'path': './Games/'})
])

print("XD")
if __name__ == "__main__":
        serv = Server()
        Server.save_to_memcached(serv)
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(address="192.168.0.10",port=8888)
        tornado.ioloop.IOLoop.instance().start()    
