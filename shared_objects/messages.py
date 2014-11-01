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


class NewPlayerConnected(Message):
    def __init__(self, player):
        self.name = player.name
        self.uuid = player.uuid
        self.position = (player.position.x, player.position.y)
        self.direction = player.direction


class PlayerInfo(Message):
    def __init__(self, player):
        self.uuid = player.uuid
        self.position = (player.position.x, player.position.y)
        self.direction = player.direction
        self.name = player.name


class PlayerMoved(Message):
    def __init__(self, uuid_, position, direction):
        self.uuid = uuid_
        self.position = position
        self.direction = direction

class PlayerDisconnected(Message):
    def __init__(self, uuid_):
        self.uuid = uuid_

class MyUID(Message):
    def __init__(self, uid):
        self.uuid = uid


class ProjectileMoved(Message):
    def __init__(self, projectile):
        self.uuid = projectile.uuid
        self.position = projectile.position


class PlayerKilled(Message):
    def __init__(self, player):
        self.uuid = player.uuid
        self.position = (player.position.x, player.position.y)
        self.direction = player.direction


