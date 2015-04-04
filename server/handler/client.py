import tornado.websocket

class ClientHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, handler):
        self = handler

    def on_message(self, message):
        print("CLIENT HANDLER")
        print("New User")
        print("Check if exist?")

    def make_response(self, request, answer):
        #request.write_message(answer)

        self.write_message("R")

    def handle_request(self, request):
        print("RAFALEK")
        import time
        time.sleep(200)
        make_response(request, "R")
        mess = {'message': 'connectSuccess', 'data': {'player_id': 55676488}}
        mess = {"message": "gameList", "data": {"game_list": [{"name": "Demo", "description": "Demo Game", "version": "0.0.1", "author": "Wolodija"}]}}
        mess = {"message": "rooms", "data": {"rooms": [[55349088, "Magiczny Krzysztof", 1, 8, "Magiczny Pokoj"]]}}
        print(self)
        print("SEND")
        print(mess)
        self.write_message(mess)


    def make_player_ready(self, player_id):
        server = Server.get_from_memcached()
        server.make_player_ready(player_id)
        return True

    def send_id_to_player(self):
        response = {'message': "connectSuccess",
            'data': {
                    'player_id': self.player.id
                }
            }
        print("Send response:")
        print(response)
        self.write_message(response)
