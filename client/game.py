import sys
import os
import pickle

import pygame
from ws4py.client.threadedclient import WebSocketClient


class Player(object):
    def __init__(self):
        self.x = 5.0
        self.y = 50.0
        self.direction = 0.0
        self._sprite = pygame.image.load(os.path.join("pyro.png")).convert_alpha()

    def render(self, game_surface):
        """game_surface: surface on which draw player sprite"""
        game_surface.blit(self._sprite, (self.x, self.y))


class WSConnection(WebSocketClient):
    def opened(self):
        pass

    def received_message(self, m):
        message = pickle.loads(str(m))
        print 'after parse: ', message.data


class Game(object):
    def __init__(self, window_caption="this is a game"):
        pygame.init()
        self._WINDOW_WIDTH = 800
        self._WINDOW_HEIGHT = 600
        self._FPS = 80  # TODO: sync with server update rate
        self._display_surf = pygame.display.set_mode((self._WINDOW_WIDTH, self._WINDOW_HEIGHT), pygame.HWSURFACE)
        pygame.display.set_caption(window_caption)
        self._running = True
        self.clock = pygame.time.Clock()
        self.connection = WSConnection("ws://127.0.0.1:8000/ws")
        self.connection.connect()
        self.p = Player()

    def _render(self):
        # TODO: call render func on objs, and pass _display_surf
        # _display_surf.blit(self._image_surf, (0, 0))
        self.p.render(self._display_surf)
        pygame.display.flip()

    def _on_event(self, event):
        if event.type == pygame.QUIT:
            sys.exit()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            rotation_direction = +1.0
        if pressed_keys[pygame.K_RIGHT]:
            rotation_direction = -1.0
        if pressed_keys[pygame.K_UP]:
            movement_direction = +1.0
        if pressed_keys[pygame.K_DOWN]:
            movement_direction = -1.0


    def run(self):
        while self._running:
            # set FPS cap
            self.clock.tick(self._FPS)

            # Events
            for event in pygame.event.get():
                self._on_event(event)

            # Render
            self._render()


if __name__ == "__main__":
    game = Game()
    game.run()
