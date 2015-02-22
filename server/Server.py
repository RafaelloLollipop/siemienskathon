from Room import Room
import jsonpickle
import json
import memcache
from random import randint
class Server(object):
    def __init__(self):
        self.rooms = []
        self.games_list = []
        self.players = []

    def create_room(self, admin_player_id, room_name):
        new_room = Room(admin_player_id, room_name)
        new_room.add_player(admin_player_id)
        self.rooms.append(new_room)
        Server.save_to_memcached(self)
        print("Create room")

    def destroy_room(self, room):
        self.rooms.destroy(room)
        Server.save_to_memcached(self)

    def delete_player(self, del_player_id):
        temp = None
        for player in self.players:
            if player.id == del_player_id:
                temp = player
        if temp is not None:
            self.players.remove(temp)
            room = self.find_player_in_rooms(del_player_id)
            if room:
                room.remove_player(del_player_id)
        Server.save_to_memcached(self)

    def find_player_in_rooms(self, player_id):
        for room in self.rooms:
            if player_id in room.players:
                return room


    def add_player(self, player):
        self.players.append(player)
        Server.save_to_memcached(self)


    def get_room_by_id(self, room_id):
        for room in self.rooms:
            if room.id == int(room_id):
                return room

    def get_rooms_list(self):
        rooms_list =[]
        for room in self.rooms:
             rooms_list.append([room.id, self.get_player_nick(room.admin_id), len(room.players), 8, room.room_name])
        return rooms_list

    def get_player_nick(self, player_id):
        for player in self.players:
            if player_id == player.id:
                return player.nick

    def remover_player_from_room(self, player_room_id, player_id):
        room = self.get_room_by_id(player_room_id)
        room.remove_player(player_id)
        Server.save_to_memcached(self)

    def add_player_to_room(self, room_id, player_id):
        room = self.get_room_by_id(room_id)
        room.add_player(player_id)
        Server.save_to_memcached(self)




    @staticmethod
    def get_from_memcached():
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        server_string = mc.get('server_mem')
        frozen = json.loads(server_string)
        server_object = jsonpickle.decode(frozen)
        return server_object
    @staticmethod
    def save_to_memcached(server):
        frozen = jsonpickle.encode(server)
        server_string = json.dumps(frozen)
        mc = memcache.Client(['127.0.0.1:11211'], debug=1)
        mc.set('server_mem', server_string)