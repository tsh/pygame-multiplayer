import sys
import json
import pickle

import pygame
from ws4py.client.threadedclient import WebSocketClient

from shared_objects.base_player import BasePlayer


class BasePlayer(object):
    STATE_IDLE  = 1
    STATE_MOVE  = 2
    STATE_SWING = 3
    STATE_HURT  = 4

    def __init__(self, ws_connection):
        self.connected = False
        self.name = "Test_1"
        self.ws_connection = ws_connection

        self.state = None  # last known state
        self.time = None  # Time of last update
        self.latency = 0  # Half of roundtrip latency in ms

        self.pos_x = 0
        self.pos_y = 0
        self.direction = 0  # Angle facing

        #TODO: set correct path
        self.sprite = pygame.image.load(r"C:\Users\TSH\PycharmProjects\pyGameMultiplayer\client\pyro.png").convert_alpha()

        self.previous_action = None

    def update_movement(self, event):
        """
        :event: pygame event
        """
        if event.key == pygame.K_LEFT:
            self.ws_connection.send(json.dumps({"mtype":"move", "direction": "LEFT"}))

        if event.key == pygame.K_RIGHT:
            self.ws_connection.send(json.dumps({"mtype":"move", "direction": "RIGHT"}))


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
