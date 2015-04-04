import tornado.httpserver
import tornado.websocket
import tornado.web
import json
from handler.client import ClientHandler
from handler.server import ServerHandler
from handler.room import RoomHandler

class ConnectionHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('new connection')

    def on_message(self, message):
        print("Connection Handler from {0} recived".format(self.request.remote_ip))
        parsed_message = tornado.escape.json_decode(message)
        #print(json.dumps(parsed_message, indent=4))
        self.handle_request(parsed_message)

    def on_close(self):
        print("close")
        #server = Server.get_from_memcached()
        #server.delete_player(self.player.id)

    def write_respone(self, response):
        self.write_message(response)

    def handle_request(self, request):
        response = {'message': "I don't understand you",
                    'data': {}}
        module_name = request['message']
        encapsulated_request = request['data']
        if module_name == 'clientModule':
            ClientHandler(self).on_message(encapsulated_request)
        elif module_name == 'serverModule':
            ServerHandler(self).on_message(encapsulated_request)
        elif module_name == 'roomModule':
            RoomHandler(self).on_message(encapsulated_request)
        else:
            self.write_respone(response)
        return

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
            player_id = data['data']['player_id']
            room_id = data['data']['room_id']
            self.make_player_ready(player_id)
            self.check_ready_flag_in_room(room_id)
            #response = self.all_ready()
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

        if data['message'] == 'gameData':
            pass
        return response

    def check_origin(self, origin):
        return True

