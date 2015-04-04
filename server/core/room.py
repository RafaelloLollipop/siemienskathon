class Room(object):
    def __init__(self, admin_id, room_name):
        self.id = id(self)
        self.room_name = room_name
        self.admin_id = admin_id
        self.max_players = 8
        self.players = []
        self.game = None

    def add_player(self, player_id):
        if player_id not in self.players:
            self.players.append(player_id)

    def remove_player(self, player_id):
        if player_id in self.players:
            self.players.remove(player_id)

    def add_game(self, game):
        self.game = game

    @staticmethod
    def get_from_memcached(room_id):
        pass

    def save_to_memcached(self):
        pass
    pass