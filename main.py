import sys
import json
import pickle

import pygame
from ws4py.client.threadedclient import WebSocketClient

from shared_objects.base_player import BasePlayer

class WSClass(WebSocketClient):
    def opened(self):
        pass

    def received_message(self, m):
        message = pickle.loads(str(m))
        print 'after parse: ', message.data

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
ws.send(json.dumps({'mtype':'test'}))

RUNNING = True
while RUNNING:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Keys
    if event.type == pygame.KEYDOWN:
        player.update_movement(event)

    # Render
    surface.fill(background_color)
    surface.blit(player.sprite, (player.pos_x,player.pos_y))
    pygame.display.flip()
