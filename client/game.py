import sys
import os
import pickle

import pygame
from ws4py.client.threadedclient import WebSocketClient

from shared_objects.messages import StateChangeMessage


class Player(object):
    def __init__(self):
        self.direction = 0.0
        self._original_image = pygame.image.load(os.path.join("pyro.png")).convert_alpha()
        self._sprite = self._original_image
        self.rect = self._sprite.get_rect()
        self.rect.center = (200, 200)

    def turn_left(self):
        self.direction += 45
        if self.direction > 360:
            self.direction = 45

    def turn_right(self):
        self.direction -= 45
        if self.direction < 0:
            self.direction = 315

    def render(self, game_surface):
        """game_surface: surface on which draw player sprite"""
        old_center = self.rect.center  # rotation distort original image and its coordinates
        self._sprite = pygame.transform.rotate(self._original_image, self.direction)  # rotate original to prevent distortion
        self.rect = self._sprite.get_rect()
        self.rect.center = old_center  # restore original position
        # Render
        game_surface.blit(self._sprite, (self.rect.x, self.rect.y))


class WSConnection(WebSocketClient):
    def opened(self):
        pass

    def received_message(self, m):
        message = pickle.loads(str(m))
        if isinstance(message, StateChangeMessage):
            print 'after parse: ', message.direction, message.x, message.y, Stage.player.rect
            Stage.player.rect.move_ip(message.x, message.y)

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
        if pressed_keys[pygame.K_LEFT]:
            Stage.player.turn_left()
            chng_state = StateChangeMessage(Stage.player.direction)
            self.connection.send(chng_state.serialize())
        if pressed_keys[pygame.K_RIGHT]:
            Stage.player.turn_right()
            chng_state = StateChangeMessage(Stage.player.direction)
            self.connection.send(chng_state.serialize())
        if pressed_keys[pygame.K_UP]:
            movement_direction = +1.0
        if pressed_keys[pygame.K_DOWN]:
            movement_direction = -1.0
        # TODO: send only if changes from prev state


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
