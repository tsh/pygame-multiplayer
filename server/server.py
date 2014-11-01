import json
import math
import time
import pickle
import uuid

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado import websocket

from shared_objects.messages import *
from objects import Player


class App(object):
    Projectiles = []

    def __init__(self):
        self.upd_player_callback = tornado.ioloop.PeriodicCallback(self.update_players, 33)
        self.upd_projectiles_callback = tornado.ioloop.PeriodicCallback(self.update_projectiles, 33)
        self.upd_network_callback = tornado.ioloop.PeriodicCallback(self.update_network, 100)
        self.upd_latency_callback = tornado.ioloop.PeriodicCallback(self.update_latency, 10000)

    def run(self):
        self.upd_player_callback.start()
        self.upd_projectiles_callback.start()
        self.upd_network_callback.start()
        self.upd_latency_callback.start()


    def update_players(self):
        for player in WSConnectionHandler.players:
            time_elapsed = ioloop.time() - player.time

            if player.state == Player.STATE_MOVE:
                #check collision here if collision(): dx, dy = 0
                player.calculate_position(time_elapsed)
                player.time = ioloop.time()
                mes = PlayerPositionMessage((player.position.x, player.position.y), player.direction)
                player.send_message(mes)
                pmvd = PlayerMoved(player.uuid, (player.position.x, player.position.y), player.direction)
                self.notify_all_players(pmvd)
            if player.state == Player.STATE_ATTACK:
                # attack last 1 sec
                bullet = player.shoot()
                App.Projectiles.append(bullet)
                if time_elapsed > 0.3:
                    player.state = Player.STATE_IDLE
                    mes = StateChangeMessage(player.state)
                    player.send_message(mes)

            if player.state == Player.STATE_HURT:
                if time_elapsed > 1000:
                    player.state = Player.STATE_HURT
                    #TODO: create change_status message
                    #self.notify_all_players()


    def update_projectiles(self):
        for projectile in App.Projectiles:
            if projectile.is_crossed_boundary():
                App.Projectiles.remove(projectile)

            dt = ioloop.time() - projectile.time
            projectile.update(dt)
            mes = ProjectileMoved(projectile)
            self.notify_all_players(mes)


    def update_network(self):
        # Send data to the client in order ty synchronize the gameplay
        for player in WSConnectionHandler.players:
            #TODO: send change_status message about himself
            #main_player.send_message()
            pass

    def update_latency(cls):
        pass

    def notify_all_players(self, message):
        for player in WSConnectionHandler.players:
            player.send_message(message)

class WSConnectionHandler(websocket.WebSocketHandler):
    players = []

    def open(self):
        player = Player(ws_connection=self, uuid=uuid.uuid4())
        player.send_message(MyUID(player.uuid))
        mes = NewPlayerConnected(player)
        self.players.append(player)
        self.notify_players_except_self(mes)
        for p in self.players:
            p_mes = PlayerInfo(p)
            player.send_message(p_mes)


    def on_message(self, message):
        msg = pickle.loads(message)
        if isinstance(msg, StateChangeMessage):
            self.handle_state_change(msg)
        if isinstance(msg, PlayerSettings):
            self.handle_player_info(msg)

    def on_close(self):
        p = self.get_player()
        WSConnectionHandler.players.remove(p)
        m = PlayerDisconnected(p.uuid)
        self.notify_all_players(m)

    def get_player(self):
        """ Return main_player obj associated with this connection """
        for player in WSConnectionHandler.players:
            if player.ws_connection == self:
                return player

    def notify_players_except_self(self, message):
        for player in self.players:
            if player.ws_connection == self:
                continue
            player.send_message(message)

    def notify_all_players(self, message):
        for player in self.players:
            player.send_message(message)

    # --- Handlers ----
    def handle_state_change(self, msg):
        player = self.get_player()
        if player.state in Player.CHANGE_ALLOWED:
            player.state = msg.player_state
            player.rotation_direction = msg.rotation_dir
            player.movement_direction = msg.movement_dir

    def handle_player_info(self, msg):
        player = self.get_player()
        if hasattr(msg, 'name'):
            player.name = msg.name


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
    ioloop.start()
