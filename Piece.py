from board_utils import *

class Piece(object):
    def __init__(self, name, team, position, movable):
        self.name = name
        self.team = team
        self.position = position
        self.movable = movable