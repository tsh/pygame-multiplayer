import tornado

from shared_objects.base_player import BasePlayer

ioloop = tornado.ioloop.IOLoop.instance()

class Player(BasePlayer):
    def __init__(self, ws_connection):
        self.name = "Test_1"
        self.ws_connection = ws_connection

        self.state = Player.STATE_IDLE  # last known state
        self.time = ioloop.time()  # Time of last update
        self.latency = 0  # Half of roundtrip latency in ms

        self.x = 0
        self.y = 0
        self.direction = 0.0  # Angle facing
        self.speed = 1.0  # max movement speed

    def send_message(self, message):
        self.ws_connection.write_message(message.serialize())
