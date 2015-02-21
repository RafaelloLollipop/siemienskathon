import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import sys
import getopt

class ClientHandler(tornado.websocket.WebSocketHandler):


    def open(self):
        print('new connection')
        self.write_message("Hello World")

    def on_message(self, message):
        print('message received %s' % message)

    def on_close(self):
        print('connection closed')

    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r'/ws', ClientHandler),
    (r'/game', ClientHandler)
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
