import json
import math

import pygame



class BasePlayer(object):
    STATE_IDLE  = 1
    STATE_MOVE  = 2
    STATE_SWING = 3
    STATE_HURT  = 4

    CHANGE_ALLOWED = [STATE_IDLE, STATE_MOVE]

    DEFAULT_NAME = "Player"

