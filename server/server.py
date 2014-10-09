import datetime
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


class App(object):
    @classmethod
    def frame(cls):
        print len(WSConnectionHandler.players)
        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), App.frame)

    @classmethod
    def update_players(cls):
        pass

    @classmethod
    def update_network(cls):
        pass

    @classmethod
    def update_latency(cls):
        pass



class WSConnectionHandler(websocket.WebSocketHandler):
    players = []

    def open(self):
        mes = WelcomeMessage().serialize()
        self.write_message(mes)
        self.players.append(self)

    def on_message(self, message):
        m = json.loads(message)
        if m['mtype'] == 'move':
            if m['direction'] == "LEFT":
                WSConnectionHandler.x -= WSConnectionHandler.speed
            elif m['direction'] == "RIGHT":
                WSConnectionHandler.x += WSConnectionHandler.speed
            self.write_message(json.dumps({'mtype':'move', 'x':WSConnectionHandler.x, 'y':WSConnectionHandler.y}))

    def on_close(self):
        WSConnectionHandler.players.remove(self)


class TornadoWSConnection(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/ws", WSConnectionHandler)
        ]
        tornado.web.Application.__init__(self, handlers, debug=True)


if __name__ == "__main__":
    app = TornadoWSConnection()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_timeout(datetime.timedelta(milliseconds=500), App.frame)
    tornado.autoreload.start(ioloop)
    ioloop.start()
