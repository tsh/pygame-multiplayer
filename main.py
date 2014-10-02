import sys

import pygame
from ws4py.client.threadedclient import WebSocketClient

from shared_objects.base_player import BasePlayer

class WSClass(WebSocketClient):
    def opened(self):
        self.send("ws4py")

    def received_message(self, m):
        print m

background_color = (255, 255, 255)
WIDTH = 800
HEIGHT = 600
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("hello")

clock = pygame.time.Clock()
FPS = 80

ws = WSClass("ws://127.0.0.1:8000/ws")
ws.connect()
player = BasePlayer(ws)
ws.send("test")

RUNNING = True
while RUNNING:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.update(event)

    # Render
    surface.fill(background_color)
    surface.blit(player.sprite, (player.pos_x,player.pos_y))
    pygame.display.flip()
