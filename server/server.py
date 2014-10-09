import json
import math

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado import websocket

from shared_objects.messages import WelcomeMessage


class Player(object):
    STATE_IDLE  = 1
    STATE_MOVE  = 2
    STATE_SWING = 3
    STATE_HURT  = 4

    def __init__(self, ws_connection):
        self.connected = False
        self.name = "Test_1"
        self.ws_connection = ws_connection

        self.state = None  # last known state
        self.time = None  # Time of last update
        self.latency = 0  # Half of roundtrip latency in ms

        self.pos_x = 0
        self.pos_y = 0
        self.direction = 0  # Angle facing
        self.speed = 0.0  # Movement speed



class App(websocket.WebSocketHandler):
    players = []

    def open(self):
        mes = WelcomeMessage().serialize()
        self.write_message(mes)

    def on_message(self, message):
        m = json.loads(message)
        if m['mtype'] == 'move':
            if m['direction'] == "LEFT":
                App.x -= App.speed
            elif m['direction'] == "RIGHT":
                App.x += App.speed
            self.write_message(json.dumps({'mtype':'move', 'x':App.x, 'y':App.y}))

    def on_close(self):
        App.users.remove(self)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/ws", App)
        ]
        tornado.web.Application.__init__(self, handlers, debug=True)


if __name__ == "__main__":
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    ioloop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()
