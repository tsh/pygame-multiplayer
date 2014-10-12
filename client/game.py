import sys
import os

import pygame


class Player(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self._sprite = pygame.image.load(os.path.join("pyro.png")).convert_alpha()

    def render(self, game_surface):
        """game_surface: surface on which draw player sprite"""
        game_surface.blit(self._sprite, (self.x, self.y))


class Game(object):
    def __init__(self, window_caption="this is a game"):
        pygame.init()
        self._WINDOW_WIDTH = 800
        self._WINDOW_HEIGHT = 600
        self._FPS = 80
        self._display_surf = pygame.display.set_mode((self._WINDOW_WIDTH, self._WINDOW_HEIGHT), pygame.HWSURFACE)
        pygame.display.set_caption(window_caption)
        self._running = True
        self.p = Player()

    def _render(self):
        # TODO: call render func on objs, and pass _display_surf
        # _display_surf.blit(self._image_surf, (0, 0))
        self.p.render(self._display_surf)
        pygame.display.flip()

    def _on_event(self, event):
        if event.type == pygame.QUIT:
            sys.exit()

    def run(self):
        while self._running:
            # Events
            for event in pygame.event.get():
                self._on_event(event)

            # Render
            self._render()


if __name__ == "__main__":
    game = Game()
    game.run()
