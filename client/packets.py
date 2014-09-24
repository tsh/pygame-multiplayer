import json


class NetworkMessage(object):
    CREATE_PLAYER   = 1
    PLAYER_INFO     = 2
    DESTROY_PLAYER  = 3
    STATE_CHANGE    = 4
