class Room(object):
    def __init__(self, room_id):
        self.room_id = room_id
        self.players = []
        self.game

    def add_player(self, player):
        pass

    def remove_player(self, player):
        pass

    @staticmethod
    def get_from_memcached(room_id):
        pass

    def save_to_memcached(self):
        pass
    pass