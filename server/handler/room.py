import tornado.websocket

class RoomHandler(tornado.websocket.WebSocketHandler):

    def handle_request(self):
        print("RAFALEK")
        mess = {'message': 'connectSuccess', 'data': {'player_id': 55676488}}
        mess = {"message": "gameList", "data": {"game_list": [{"name": "Demo", "description": "Demo Game", "version": "0.0.1", "author": "Wolodija"}]}}
        mess = {"message": "rooms", "data": {"rooms": [[55349088, "Magiczny Krzysztof", 1, 8, "Magiczny Pokoj"]]}}
        print(self)
        print("SEND")
        print(mess)
        self.write_message(mess)

    def all_ready(self):
        game = Game.getGameByName("Demo")
        server = Server.get_from_memcached()
        #TODO
        gra = game(server.players)

        gra.doAction({'id': server.players[0].id, 'action': 'start'})

    def check_ready_flag_in_room(self, room_id):
        server = Server.get_from_memcached()
        if server.check_ready_flag_in_room(room_id):
            self.all_ready()


    def create_new_room(self, room_name):
        server = serv.get_from_memcached()
        server.create_room(self.player.id, room_name)
