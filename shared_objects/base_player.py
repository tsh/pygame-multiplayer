import json

import pygame



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
        self.speed = 0.0  # Movement speed

        #TODO: set correct path
        self.sprite = pygame.image.load(r"C:\Users\TSH\PycharmProjects\pyGameMultiplayer\client\pyro.png").convert_alpha()

        self.previous_action = None

    def update(self, event):
        """
        :event: pygame event
        """
        if self.previous_action == event.type:
            return
        self.previous_action = event.type
        self.ws_connection.send(json.dumps({"mtype":"move", "direction": self.direction}))
