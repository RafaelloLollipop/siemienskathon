import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import sys
import getopt
import json
from Room import Room



class ClientHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print('new connection')
        #self.write_message("Hello World")

    def on_message(self, message):
        print(message)
        response = self.handle_request(message)
        resp = json.dumps(response)
        print("Send response:")
        print(resp)
        self.write_message(resp)

    def handle_request(self, data):
        response = {'message': "NOPE_OK",
                        }
        data = json.loads(data)
        print(data['message'])
        if data['message'] == 'connectToServer':
            response = self.get_rooms_list_info()
            return response

        if data['message'] == 'connectToRoom':
            room = Room.get_from_memcached(data['data']['room_id'])
            #game_name = room.game.name
            game_name = "demo"
            game_script = self.request.host + "/games/" +game_name + "/" + game_name +".js"
            print(game_script)
            response = {'message': "roomUpdate",
                        'players': [],
                        'game': game_name,
                        'game_script': game_script
                        }

            return response
        if data['message'] == 'exitRoom':
            response = {'message': "OK",
                        }
            return response
        if data['message'] == 'selectGame':
            response = {'message': "OK",
                        }
            return response
        if data['message'] == 'selectGame':
            response = {'message': "OK",
                        }
            return response
        if data['message'] == 'ready':
            response = {'message': "OK",
                        }
            return response

    def get_rooms_list_info(self):
            message = "rooms"
            rooms = []
            ant = [3, 'AntekTworca', 0, 8]
            adam = [1, 'AdamTworca', 5, 8]
            raf = [2, 'RafalTworca', 0, 8]
            rooms.append(ant)
            rooms.append(adam)
            rooms.append(raf)
            response = {'message': message,
                        'rooms': rooms}
            return response

    def on_close(self):
        print('connection closed')

    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r'/game', ClientHandler),
    (r'/games/(.*)', tornado.web.StaticFileHandler, {'path': './Games/'})
])


if __name__ == "__main__":
    address = ''
    port = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ha:', ['address='])
    except getopt.GetoptError:
        print("-a address")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("HELP")
        if opt == '-a':
            address, port = arg.split(':')
    if not(address and port):
        address = '127.0.0.1'
        port = 8888
    http_server = tornado.httpserver.HTTPServer(application)
    print("Run server on {address}:{port}".format(address=address, port=port))
    http_server.listen(port=port, address=address)
    tornado.ioloop.IOLoop.instance().start()
