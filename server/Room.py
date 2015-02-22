class Room(object):
    def __init__(self, admin_id, room_name):
        self.room_id = id(self)
        self.room_name = room_name
        self.admin_id = admin_id
        self.max_players = 8
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        pass

    @staticmethod
    def get_from_memcached(room_id):
        pass

    def save_to_memcached(self):
        pass
    pass