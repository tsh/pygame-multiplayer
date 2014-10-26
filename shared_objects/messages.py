import pickle

from shared_objects.base_player import BasePlayer


class Message:
    WELCOME = 0
    CREATE_PLAYER = 1
    PLAYER_INFO = 2
    DESTROY_PLAYER = 3
    STATE_CHANGE = 4

    def serialize(self):
        return pickle.dumps(self)


class WelcomeMessage(Message):
    def __init__(self, data='welcome'):
        self.header = Message.WELCOME
        self.data = data


class StateChangeMessage(Message):
    def __init__(self, player_state=None, rotation_dir=None, movement_dir=None):
        self.header = Message.STATE_CHANGE
        self.player_state = player_state
        self.rotation_dir = rotation_dir
        self.movement_dir = movement_dir


class PlayerPositionMessage(Message):
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

class PlayerInfo(Message):
    def __init__(self, rect):
        self.rect = rect