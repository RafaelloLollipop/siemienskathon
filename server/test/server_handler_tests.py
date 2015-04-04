import unittest
import websocket
import json


class TestServerHandler(unittest.TestCase):
    def setUp(self):
        # websocket.enableTrace(True)
        self.ws = websocket.create_connection("ws://127.0.0.1:8888/")

    def test_first_connection(self):
        request = {'message': 'serverModule',
                   'data': {
                       'message': 'connectToServer',
                       'data': {
                           'player_name': 'test_nick'
                       }
                   }
        }
        json_request = json.dumps(request)
        # print("Send request:")
        #print(json_request)
        self.ws.send(json_request)
        result = self.ws.recv()
        #print("Received:")
        #print(result)
        parsed_results = json.loads(result)
        data = parsed_results['data']
        player_id = data['player_id']
        self.ws.close()
        self.assertTrue(type(player_id) is int, "Function don't return player id")

    def test_get_rooms_list(self):
        request = {'message': 'serverModule',
                   'data': {
                       'message': 'getRoomsList',
                       'data': {}
                   }
        }
        json_request = json.dumps(request)
        # print("Send request:")
        #print(json_request)
        self.ws.send(json_request)
        result = self.ws.recv()
        print("Received:")
        print(result)
        parsed_results = json.loads(result)
        data = parsed_results['data']
        #player_id = data['player_id']
        self.ws.close()
        #self.assertTrue(type(player_id) is int, "Function don't return player id")


if __name__ == '__main__':
    unittest.main()