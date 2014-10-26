import sys
import os
import pickle

import pygame
from ws4py.client.threadedclient import WebSocketClient

from shared_objects.messages import *
from shared_objects.base_player import BasePlayer


class Player(BasePlayer):
    def __init__(self):
        self.direction = 0
        self._original_image = pygame.image.load(os.path.join("pyro.png")).convert_alpha()
        self.position = (200, 150)

    def render(self, game_surface):
        rotated_sprite = pygame.transform.rotate(self._original_image, self.direction)
        w, h = rotated_sprite.get_size()
        sprite_draw_pos = (self.position[0]-w/2, self.position[1]-h/2)
        game_surface.blit(rotated_sprite, sprite_draw_pos)


class WSConnection(WebSocketClient):
    def opened(self):
        pass

    def received_message(self, m):
        message = pickle.loads(str(m))
        if isinstance(message, PlayerPositionMessage):
            print 'after parse: ', message.position
            Stage.player.position = message.position
            Stage.player.direction = message.direction

    def closed(self, code, reason=None):
        print "CLOSED", code


class Stage(object):
    player = None


class Game(object):
    def __init__(self, window_caption="this is a game"):
        pygame.init()
        self._WINDOW_WIDTH = 800
        self._WINDOW_HEIGHT = 600
        self._FPS = 60  # TODO: sync with server update rate
        self._display_surf = pygame.display.set_mode((self._WINDOW_WIDTH, self._WINDOW_HEIGHT), pygame.HWSURFACE)
        pygame.display.set_caption(window_caption)
        self._running = True
        self.clock = pygame.time.Clock()
        self.connection = WSConnection("ws://127.0.0.1:8000/ws")
        self.connection.connect()
        Stage.player = Player()

    def _render(self):
        self._display_surf.fill((1, 2, 2))
        # TODO: call render func on objs, and pass _display_surf
        # _display_surf.blit(self._image_surf, (0, 0))
        Stage.player.render(self._display_surf)
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
        self.connection.send(chng_state.serialize())


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
