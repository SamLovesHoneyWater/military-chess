from board_utils import *

class JunqiBoard:
    def __init__(self):
        # Define the dimensions of the board
        self.rows = 12
        self.columns = 5

        # Initialize the board with empty spaces
        self.terrain_board = [[LAND for _ in range(self.columns)] for _ in range(self.rows)]

        self.place_rails()

        # Place the lakes on the board
        self.place_lakes()

        # Place the traps on the board
        #self.place_traps()

        # Place the flags and bombs on the board
        self.place_flags_and_bombs()

    def place_rails(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if (col == 0 or col == self.columns-1) and (row !=0 and row != self.rows-1):
                    self.terrain_board[row][col] = RAIL
                elif row in [1, 5, 6, 10]:
                    self.terrain_board[row][col] = RAIL

    def place_lakes(self):
        # Lakes are represented by 'X' on the board
        lake_positions = [(2, 1), (2, 3),
                              (3, 2),
                          (4, 1), (4, 3),
                          (7, 1), (7, 3),
                              (8, 2),
                          (9, 1), (9, 3)]
        for row, col in lake_positions:
            self.terrain_board[row][col] = LAKE

    def place_flags_and_bombs(self):
        flag_positions = [(0, 1), (0, 3), (11, 1), (11, 3)]
        for row, col in flag_positions:
            self.terrain_board[row][col] = BASE

    def print_terrain_board(self):
        # Print the base terrain board
        for row in self.terrain_board:
            print(' '.join(row))

# Example usage:
board = JunqiBoard()
board.print_terrain_board()
print(board.terrain_board)