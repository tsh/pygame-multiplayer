import sys
import os
import pickle

import pygame
from ws4py.client.threadedclient import WebSocketClient

from game_config import GameConfig
from shared_objects.messages import *
from shared_objects.base_player import BasePlayer


class Player(BasePlayer):
    def __init__(self):
        self.name = None
        self.uuid = None
        self.direction = 0
        self._original_image = pygame.image.load(os.path.join("pyro.png")).convert_alpha()
        self.position = (200, 150)

    def render(self, game_surface):
        rotated_sprite = pygame.transform.rotate(self._original_image, self.direction)
        w, h = rotated_sprite.get_size()
        sprite_draw_pos = (self.position[0]-w/2, self.position[1]-h/2)
        game_surface.blit(rotated_sprite, sprite_draw_pos)

    def init_player_from_mes(self, message):
        if isinstance(message, PlayerInfo):
            self.uuid = message.uuid
            self.position = message.position
            self.direction = message.direction
            self.name = message.name
        else:
            raise Exception

    def update_position_f_message(self, message):
        if isinstance(message, PlayerMoved):
            self.position = message.position
            self.direction = message.direction


class WSConnection(WebSocketClient):
    def opened(self):
        pi = PlayerSettings(name=GameConfig.player_default_name)
        Stage.send_message(pi)

    def received_message(self, m):
        message = pickle.loads(str(m))
        if isinstance(message, NewPlayerConnected):
            player = Player()
            player.name = message.name
            player.uuid = message.uuid
            player.position = message.position
            player.direction = message.direction
            Stage.players[player.uuid] = player
        if isinstance(message, PlayerInfo):
            p = Player()
            p.init_player_from_mes(message)
            Stage.players[p.uuid] = p
        if isinstance(message, PlayerMoved):
            try:
                player = Stage.players[message.uuid]
            except KeyError:
                return
            player.update_position_f_message(message)


    def closed(self, code, reason=None):
        print "CLOSED", code


class Stage(object):
    connection = None
    players = {}

    @classmethod
    def send_message(cls, message):
        cls.connection.send(message.serialize())

class Game(GameConfig):
    def __init__(self, window_caption="this is a game"):
        pygame.init()
        self._WINDOW_WIDTH = 800
        self._WINDOW_HEIGHT = 600
        self._FPS = 60  # TODO: sync with server update rate
        self._display_surf = pygame.display.set_mode((self._WINDOW_WIDTH, self._WINDOW_HEIGHT), pygame.HWSURFACE)
        pygame.display.set_caption(window_caption)
        self._running = True
        self.clock = pygame.time.Clock()
        Stage.connection = WSConnection("ws://127.0.0.1:8000/ws")
        Stage.connection.connect()


    def _render(self):
        self._display_surf.fill((1, 2, 2))
        for player in Stage.players.values():
            player.render(self._display_surf)

        pygame.display.flip()

    def _on_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _movement(self):
        pressed_keys = pygame.key.get_pressed()
        rotation_direction = 0
        movement_direction = 0

        if pressed_keys[pygame.K_LEFT]:
            rotation_direction += 1

        if pressed_keys[pygame.K_RIGHT]:
            rotation_direction -= 1

        if pressed_keys[pygame.K_UP]:
            movement_direction -= 1

        if pressed_keys[pygame.K_DOWN]:
            movement_direction += 1

        # TODO: send only if changes from prev state
        chng_state = StateChangeMessage(BasePlayer.STATE_MOVE, rotation_direction, movement_direction)
        Stage.send_message(chng_state)


    def run(self):
        while self._running:
            # set FPS cap
            self.clock.tick(self._FPS)

            # Events
            self._on_event()

            # Movement
            self._movement()

            # Render
            self._render()


if __name__ == "__main__":
    game = Game()
    game.run()
