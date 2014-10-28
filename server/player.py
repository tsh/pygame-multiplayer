import math

import tornado

from shared_objects.base_player import BasePlayer
from shared_objects.vector2 import Vector2

ioloop = tornado.ioloop.IOLoop.instance()


class Player(BasePlayer):
    def __init__(self, ws_connection, uuid):
        self.name = "Test_1"
        self.ws_connection = ws_connection
        self.uuid = uuid

        self.state = Player.STATE_IDLE  # last known state
        self.time = ioloop.time()  # Time of last update
        self.latency = 0  # Half of roundtrip latency in ms

        self.position = Vector2(200, 200)
        self.direction = 0.0  # Angle facing
        self.rotation_speed = 45
        self.movement_speed = 50
        self.movement_direction = 0
        self.rotation_direction = 0



    def calculate_position(self, time_passed):
        self.direction += self.rotation_direction * self.rotation_speed * time_passed

        dx = math.sin(self.direction * math.pi / 180)
        dy = math.cos(self.direction * math.pi / 180)
        move_vector = Vector2(dx, dy)
        move_vector *= self.movement_direction
        self.position += move_vector * self.movement_speed * time_passed


    def send_message(self, message):
        self.ws_connection.write_message(message.serialize())
