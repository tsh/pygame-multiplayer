import math
import uuid

import tornado

from shared_objects.base_player import BasePlayer
from shared_objects.vector2 import Vector2
from server_config import GameConfig
from shared_objects.messages import PlayerKilled

ioloop = tornado.ioloop.IOLoop.instance()


class Player(BasePlayer):
    player_rect = None  # hold player rectangle for collision detection

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

        self.rect = Player.player_rect
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def calculate_position(self, time_passed):
        self.direction += self.rotation_direction * self.rotation_speed * time_passed

        dx = math.sin(self.direction * math.pi / 180)
        dy = math.cos(self.direction * math.pi / 180)
        move_vector = Vector2(dx, dy)
        move_vector *= self.movement_direction *-1  # magic -1 for correct movement
        self.position += move_vector * self.movement_speed * time_passed

        self.rect.x = self.position.x
        self.rect.y = self.position.y


    def send_message(self, message):
        self.ws_connection.write_message(message.serialize())

    def shoot(self):
        bullet = Projectile((self.position.x, self.position.y), self.direction, self)
        return bullet

    def handle_hit(self):
        mes = PlayerKilled(self)
        self.send_message(mes)

class Projectile(object):
    rect = None

    def __init__(self, position, angle, shooter):
        """
        :position: tuple of x,y values
        :angle: in grad
        """
        self.position = position
        self.angle = angle
        self.speed = 120
        self.shooter = shooter

        self.time = ioloop.time()
        self.uuid = uuid.uuid4()

        self.rect = Projectile.rect
        self.rect.x, self.rect.y = self.position

    def update(self, dt):
        dx = math.sin(self.angle * math.pi / 180) * self.speed * dt
        dy = math.cos(self.angle * math.pi / 180) * self.speed * dt
        self.position = (self.position[0] + dx, self.position[1] + dy)
        self.rect.x, self.rect.y = self.position

    def is_crossed_boundary(self):
        """ Check if bullet is outside game world
        """
        if self.position[0] > GameConfig.GAME_WORLD_SIZE[0] or self.position[0] < 0 or \
           self.position[1] > GameConfig.GAME_WORLD_SIZE[1] or self.position[1] < 0:
            return True
        else:
            return False
