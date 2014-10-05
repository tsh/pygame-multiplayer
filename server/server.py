import json
import math

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado import websocket


class WSHandler(websocket.WebSocketHandler):
    users = []
    x = 0
    y = 0
    speed = 5.0
    direction = 0

    def open(self):
        WSHandler.users.append(self)

    def on_message(self, message):
        m = json.loads(message)
        if m['mtype'] == 'move':
            if m['direction'] == "LEFT":
                WSHandler.x -= WSHandler.speed
            elif m['direction'] == "RIGHT":
                WSHandler.x += WSHandler.speed
            self.write_message(json.dumps({'mtype':'move', 'x':WSHandler.x, 'y':WSHandler.y}))

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
