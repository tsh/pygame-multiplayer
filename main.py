import sys
import websocket
import pygame

from shared_objects.base_player import BasePlayer

background_color = (255, 255, 255)
WIDTH = 800
HEIGHT = 600
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("hello")

player = BasePlayer()
ws = websocket.create_connection("ws://127.0.0.1:8000/ws")
ws.send("test")
print ws.recv()

RUNNING = True
while RUNNING:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pass

    # Render
    surface.fill(background_color)
    surface.blit(player.sprite, (player.pos_x,player.pos_y))
    pygame.display.flip()
