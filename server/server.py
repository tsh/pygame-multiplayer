import json
import math
import time
import pickle

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado import websocket

from shared_objects.messages import *
from player import Player


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
                player.x += dx
                player.y += dy
                player.time = ioloop.time()
                mes = PlayerPositionMessage(player.x, player.y, player.direction)
                player.send_message(mes)
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
        msg = pickle.loads(message)
        if isinstance(msg, StateChangeMessage):
            self.handle_state_change(msg)

    def on_close(self):
        p = self.get_player()
        WSConnectionHandler.players.remove(p)

    def get_player(self):
        """ Return player obj associated with this connection """
        for player in WSConnectionHandler.players:
            if player.ws_connection == self:
                return player

    def handle_state_change(self, msg):
        player = self.get_player()
        if player.state in Player.CHANGE_ALLOWED:
            player.state = msg.player_state
            player.direction = msg.direction
        # player.direction = msg.direction
        # dx = math.cos(math.radians(player.direction)) * player.speed
        # dy = math.sin(math.radians(player.direction)) * player.speed
        # player.x += dx
        # player.y += dy
        # mes = StateChangeMessage(player.direction, player.x, player.y)
        # self.write_message(mes.serialize())


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
