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


class StateChangeMessage(Message):
    def __init__(self, player_state=None, rotation_dir=None, movement_dir=None):
        self.header = Message.STATE_CHANGE
        self.player_state = player_state
        self.rotation_dir = rotation_dir
        self.movement_dir = movement_dir


class PlayerPositionMessage(Message):
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction


class PlayerSettings(Message):
    def __init__(self, name=BasePlayer.DEFAULT_NAME, game_class=None, rect=None):
        self.name = name
        self.game_class = game_class
        self.rect = rect
