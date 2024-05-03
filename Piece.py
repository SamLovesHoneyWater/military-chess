from board_utils import *

class Piece(object):
    def __init__(self, name, team, position, moveable):
        self.name = name
        self.team = team  # relative team information: 0 = opponent, 1 = friendly
        #self.position = position
        self.moveable = moveable
        if self.name == FLAG:
            self.do_display = False
