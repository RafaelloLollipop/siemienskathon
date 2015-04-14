import unittest
import websocket
import json


class TestServerHandler(unittest.TestCase):
    def setUp(self):
        # websocket.enableTrace(True)
        self.ws = websocket.create_connection("ws://127.0.0.1:8888/")

    def tearDown(self):
        pass#self.ws.close()

    def get_connection_request(self):
        request = {'message': 'serverModule',
                   'data': {
                       'message': 'connectToServer',
                       'data': {
                           'player_name': 'test_nick'
                       }
                   }
        }
        return request

    def get_create_random_room_request(self):
        import random

        number = random.randint(1, 2000)
        request = {
            'message': 'serverModule',
            'data': {
                'message': 'createNewRoom',
                'data': {
                    'room_name': number,
                    'creator_id': 2
                }
            }
        }

    def test_first_connection(self):
        request = self.get_connection_request()
        json_request = json.dumps(request)
        self.ws.send(json_request)
        result = self.ws.recv()
        parsed_results = json.loads(result)
        print(result)
        # data = parsed_results['data']
        #player_id = data['player_id']
        #self.assertTrue(type(player_id) is int, "Function don't return player id")

    def dtest_add_random_room(self):
        request = self.get_create_random_room_request()
        json_request = json.dumps(request)
        self.ws.send(json_request)
        result = self.ws.recv()
        parsed_results = json.loads(result)
        data = parsed_results['data']
        player_id = data['player_id']
        self.assertTrue(type(player_id) is int, "Function don't return player id")

    def dtest_get_rooms_list(self):
        request = {'message': 'serverModule',
                   'data': {
                       'message': 'getRoomsList',
                       'data': {}
                   }
        }
        json_request = json.dumps(request)
        self.ws.send(json_request)
        result = self.ws.recv()
        parsed_results = json.loads(result)
        data = parsed_results['data']
        player_id = data['player_id']
        self.assertTrue(type(player_id) is int, "Function don't return player id")


    def dtest_add_user(self):
        client_list = self.read_user_memory()
        print(client_list)


    def read_user_memory(self):
        from multiprocessing.managers import BaseManager

        class ListManager(BaseManager): pass

        ListManager.register('get_client_list')
        m = ListManager(address=('localhost', 50000), authkey=123)
        m.connect()
        l = m.get_client_list()
        return l


if __name__ == '__main__':
    unittest.main()