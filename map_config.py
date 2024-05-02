from board_utils import *
from Piece import Piece

def file_to_lines(file_name):
	with open(file_name, encoding="utf-8") as f:
		lines = f.readlines()
		for i, line in enumerate(lines):
			line = ' '.join(line.split())
			lines[i] = line
	return lines

def text_to_lines(text):
	lines = text.split('\n')
	for i, line in enumerate(lines):
		line = ' '.join(line.split())
		lines[i] = line
	return lines

def lines_to_board(lines):
	if len(lines) != len(HALF_TERRAIN):
		raise ValueError("Incorrect lines given, need to be like HALF_TERRAIN, but got", lines)
	board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS//2)]

	name_counts = {ZONG: 0, JUN: 0, SHI: 0, LV: 0, TUAN: 0, YING: 0,
				   LIAN: 0, PAI: 0, GONG: 0, TRAP: 0, BOMB: 0, FLAG: 0}

	for row, line in enumerate(lines):
		piece_names = line.split()
		col = 0
		for name in piece_names:
			# Check for value correctness
			if name not in ALL_PIECE_NAMES:
				raise ValueError("Unexpected piece name", name)
			if col >= BOARD_COLS:
				raise ValueError("To many pieces in row", line)

			# Skip lakes during initial placement
			if HALF_TERRAIN[row][col] == LAKE:
				col += 1

			# Flag must be in one of the bases 
			if name == FLAG and HALF_TERRAIN[row][col] != BASE:
				raise ValueError("Flag must be placed in base, but this is violated in row", line)

			# Trap must be in last two rows
			if name == TRAP and row < BOARD_ROWS//2 - 2:
				raise ValueError("Trap must be placed in the last two rows, but this is violated in row", line)

			# Bomb must not be in first rows
			if name == BOMB and row == 0:
				raise ValueError("Bomb must not be placed in the first row, but this is violated in row", line)

			# Pieces in bases cannot move
			if HALF_TERRAIN[row][col] == BASE:
				movable = False
			else:
				movable = True

			new_piece = Piece(name, 0, (row, col), movable)
			board[row][col] = new_piece
			name_counts[name] += 1
			col += 1

		# Check that current row is saturated
		if col != 5:
			raise ValueError("Insufficient number of pieces in row", line)

	# Check that piece counts are correct
	for name in ALL_PIECE_NAMES:
		if name_counts[name] != PIECE_INITIAL_NUMBERS[name]:
			raise ValueError("Count of pieces incorrect for piece name", name,
				"expected", PIECE_INITIAL_NUMBERS[name], "but got", name_counts[name])
	return board

def init_full_board(my_board, opponent_board):
	board = []
	
	opponent_board.reverse()
	for i, row in enumerate(opponent_board):
		for piece in row:
			if piece is None:
				continue
			piece.position = (i, piece.position[1])
		board.append(row)

	for i, row in enumerate(my_board):
		for piece in row:
			if piece is None:
				continue
			piece.position = (i + BOARD_ROWS//2, piece.position[1])
		board.append(row)

	return board

setup_folder = 'setups/'
lines1 = file_to_lines(setup_folder + 'setup1.txt')
lines2 = file_to_lines(setup_folder + 'setup2.txt')
opponent_half_board = lines_to_board(lines1)
my_half_board = lines_to_board(lines2)
board = init_full_board(my_half_board, opponent_half_board)
pretty_print_board(board)

while True:
	turn = 
