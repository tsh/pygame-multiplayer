import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado import websocket


class WSHandler(websocket.WebSocketHandler):
    users = []

    def open(self):
        WSHandler.users.append(self)

    def on_message(self, message):
        print message
        self.write_message("You say: " + message)

    def on_close(self):
        WSHandler.users.remove(self)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/ws", WSHandler)
        ]
        tornado.web.Application.__init__(self, handlers, debug=True)


if __name__ == "__main__":
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    ioloop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()
