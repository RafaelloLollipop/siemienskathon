from Room import Room


class Server(object):
    def __init__(self):
        self.rooms = []
        self.games_list = []

    def create_room(self):
        pass

    def destroy_room(self):
        pass

    @staticmethod
    def get_from_memcached():
        pass

    def save_to_memcached(self):
        pass
    pass