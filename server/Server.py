from Room import Room
import jsonpickle
import json
import memcache
from random import randint
class Server(object):
    def __init__(self):
        self.rooms = []
        self.games_list = []

    def create_room(self, admin_player, room_name):
        new_room = Room(admin_player.id, room_name)
        new_room.add_player(admin_player)
        self.rooms.append(new_room)
        Server.save_to_memcached(self)
        print("Create room")

    def destroy_room(self):
        pass

    def get_room_by_id(self, room_id):
        for room in self.rooms:
            if room.room_id == int(room_id):
                print("TRUE")
                return room


    def get_rooms_list(self):
        rooms_list =[]
        for room in self.rooms:
             rooms_list.append([room.room_id, "rf", len(room.players), 8, room.room_name])
        return rooms_list


    @staticmethod
    def get_from_memcached():
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        server_string = mc.get('server_mem')
        frozen = json.loads(server_string)
        server_object = jsonpickle.decode(frozen)
        return server_object
    @staticmethod
    def save_to_memcached(server):
        print("R")
        frozen = jsonpickle.encode(server)
        print("R")
        server_string = json.dumps(frozen)
        print("R")
        mc = memcache.Client(['127.0.0.1:11211'], debug=1)
        mc.set('server_mem', server_string)