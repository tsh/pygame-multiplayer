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

        self.state = Player.STATE_IDLE  # last known state
        self.time = ioloop.time()  # Time of last update
        self.latency = 0  # Half of roundtrip latency in ms

        self.pos_x = 0
        self.pos_y = 0
        self.direction = 0.0  # Angle facing
        self.speed = 5.0  # Movement speed

    def send_message(self, message):
        self.ws_connection.write_message(message)


class App(object):
    def __init__(self):
        self.upd_player_callback = tornado.ioloop.PeriodicCallback(self.update_players, 33)
        self.upd_network_callback = tornado.ioloop.PeriodicCallback(self.update_network, 100)
        self.upd_latency_callback = tornado.ioloop.PeriodicCallback(self.update_latency, 10000)

    def run(self):
        self.upd_player_callback.start()
        self.upd_network_callback.start()
        self.upd_latency_callback.start()


    def update_players(self):
        for player in WSConnectionHandler.players:
            time_elapsed = ioloop.time() - player.time

            if player.state == Player.STATE_MOVE:
                speed = time_elapsed * player.speed
                dx = math.sin(player.direction) * speed
                dy = math.cos(player.direction) * speed
                #check collision here if collision(): dx, dy = 0
                player.pos_x += dx
                player.pos_y += dy
                player.time = ioloop.time()
                #TODO: create move message
                #self.notify_all_players()

            if player.state == Player.STATE_SWING:
                # swing last 1 sec
                if time_elapsed > 1000:
                    player.state = Player.STATE_IDLE
                    #TODO: create change_status message
                    #self.notify_all_players()

            if player.state == Player.STATE_HURT:
                if time_elapsed > 1000:
                    player.state = Player.STATE_HURT
                    #TODO: create change_status message
                    #self.notify_all_players()

    def update_network(self):
        # Send data to the client in order ty synchronize the gameplay
        for player in WSConnectionHandler.players:
            #TODO: send change_status message about himself
            #player.send_message()
            pass

    def update_latency(cls):
        pass

    def notify_all_players(self, message):
        for player in WSConnectionHandler.players:
            player.send_message(message)



class WSConnectionHandler(websocket.WebSocketHandler):
    players = []

    def open(self):
        mes = WelcomeMessage().serialize()
        self.write_message(mes)
        player = Player(ws_connection=self)
        self.players.append(player)

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
    app = App()
    app.run()
    ioloop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()
