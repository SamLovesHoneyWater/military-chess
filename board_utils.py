LAKE = '〇'
BASE = '凸'
RAIL = '十'
LAND = '口'

ZONG = '司令'
JUN = '军长'
SHI = '师长'
LV = '旅长'
TUAN = '团长'
YING = '营长'
LIAN = '连长'
PAI = '排长'
GONG = '工兵'
TRAP = '地雷'
BOMB = '炸弹'
FLAG = '军旗'

SECRET_PIECE = '████'

ALL_PIECE_NAMES = [
				ZONG,
				JUN,
				SHI,
				LV,
				TUAN,
				YING,
				LIAN,
				PAI,
				GONG,
				TRAP,
				BOMB,
				FLAG
				]

PIECE_INITIAL_NUMBERS = {
			ZONG: 1,
			JUN: 1,
			SHI: 2,
			LV: 2,
			TUAN: 2,
			YING: 2,
			LIAN: 3,
			PAI: 3,
			GONG: 3,
			TRAP: 3,
			BOMB: 2,
			FLAG: 1
		}

PIECE_RANKING = {ZONG: 9,
				 JUN: 8,
				 SHI: 7,
				 LV: 6,
				 TUAN: 5,
				 YING: 4,
				 LIAN: 3,
				 PAI: 2,
				 GONG: 1,
				 FLAG: 0,
				 TRAP: -1,
				 BOMB: -2}

def pretty_print(board):
	for row in board:
		print(' '.join(row))

def pretty_print_board(board):
	for row in board:
		names = []
		for piece in row:
			if piece is None:
				# Lake
				names.append("（）")
			else:
				names.append(piece.name)
		print(' '.join(names))

BOARD_COLS = 5
BOARD_ROWS = 12

BASE_COLS = [1, 3]

HALF_TERRAIN = [
				[RAIL, RAIL, RAIL, RAIL, RAIL],
				[RAIL, LAKE, LAND, LAKE, RAIL],
				[RAIL, LAND, LAKE, LAND, RAIL],
				[RAIL, LAKE, LAND, LAKE, RAIL],
				[RAIL, RAIL, RAIL, RAIL, RAIL],
				[LAND, BASE, LAND, BASE, LAND]
			]

other_half_terrain = HALF_TERRAIN.copy()
other_half_terrain.reverse()
FULL_TERRAIN = other_half_terrain + HALF_TERRAIN

for col in BASE_COLS:
	assert(HALF_TERRAIN[-1][col]) == BASE

pretty_print(HALF_TERRAIN)

def display_board(board, secret=True):
	divider = "————————————————————————"
	print(divider)
	for row, pieces in enumerate(board):
		pre_row_display = "    "
		row_display = " "
		if row < 9:
			# Add an extra space for one-digit row number for formatting
			row_display += ' '
		row_display += str(row + 1)
		row_display += ' '
		post_row_display = "    "
		for col, piece in enumerate(pieces):
			# Add terrain effects
			if FULL_TERRAIN[row][col] == LAKE:
				row_display += "（"
				pre_row_display += "  ----  "
				post_row_display += "  ----  "
			elif FULL_TERRAIN[row][col] == BASE:
				row_display += "||"
				pre_row_display += "  ====  "
				post_row_display += "  ====  "
			else:
				row_display += "  "
				pre_row_display += "        "
				post_row_display += "        "

			# Add actual piece name to display
			if piece is None:
				row_display += "    "
			elif not secret or piece.team or (piece.name == FLAG and piece.do_display):
				row_display += piece.name
			else:
				row_display += SECRET_PIECE

			# Add terrain effects
			if FULL_TERRAIN[row][col] == LAKE:
				row_display += "）"
			elif FULL_TERRAIN[row][col] == BASE:
				row_display += "||"
			else:
				row_display += "  "
		print(pre_row_display)
		print(row_display)
		print(post_row_display)
	print(divider)

def get_all_reacheable(board, x1, y1):


def can_move_from(board, x1, y1):
	# Check if coords are within bounds
	if not 0 <= y1 < BOARD_ROWS or not 0 <= x1 < BOARD_COLS:
		return (False, "Invalid selection! Row or column number out of bounds.")

	piece = board[y1][x1]

	if not piece.team:
		return (False, "Invalid selection! You can only move your own piece.")

	if not piece.moveable:
		return (False, "Invalid selection! You cannot move an unmoveable piece.")

	return (True, "Piece selected!")

def can_move_to(board, x1, y1, x2, y2):
	# Check if coords are within bounds
	if not 0 <= y1 < BOARD_ROWS or not 0 <= x1 < BOARD_COLS:
		return (False, "Invalid selection! Row or column number out of bounds.")
	if not 0 <= y2 < BOARD_ROWS or not 0 <= x2 < BOARD_COLS:
		return (False, "Invalid target location! Row or column number out of bounds.")

	if y1 == y2 and x1 == x2:
		return (False, "Invalid move! You cannot move a piece to its current location.")

	piece = board[y1][x1]
	target_piece = board[y2][x2]

	if not piece.moveable:
		return (False, "Invalid selection! You cannot move an unmoveable piece.")

	if not ((x2, y2) in get_all_reacheable(board, x1, y1)):
		return (False, "Invalid move! There is no viable path to the target location.")

	# Target obstructed by friendly
	if (target_piece is not None) and (piece.team == target_piece.team):
		return (False, "Invalid move! A friendly piece is already on that tile.")

	# Target is an occupied lake
	if (target_piece is not None) and (FULL_TERRAIN[y2][x2] == LAKE):
		return (False, "Invalid move! You cannot attack an enemy that is in a lake.")

	return (True, "Move taken!")

'''
Compares two pieces
Input
	subject :: Piece = the piece whose outcome we are interested in
	target :: Piece = the piece being compared against
Output :: Int in [0,2] where 0 means subject lost, 1 means subject won,and 2 means both sides
are destroyed
'''
def cmp_piece(subject, target):
	if subject.team == target.team:
		raise ValueError("Comparing the force of pieces on the same team!")
	rank_subject, rank_target = PIECE_RANKING[subject.name], PIECE_RANKING[target.name]
	if rank_subject == -2 or rank_target == -2:  # Bombed
		return 2
	elif rank_subject == -1 and rank_target != 1:  # Subject trapped the opponent
		return 1
	elif rank_subject != 1 and rank_target == -1:  # Subject is trapped
		return 0
	elif rank_subject == rank_target:  # Equal force
		return 2
	elif rank_subject > rank_target:  # Won
		return 1
	else:  # Lost
		return 0

'''
Eliminates a tile on the board
Input
	board :: 2D list = the full piece board of current game
	x :: Int in [0, BOARD_COLS] = the col of the piece to be eliminated
	y :: Int in [0, BOARD_ROWS] = the row of the piece to be eliminated
Output :: board :: Updated board
'''
def eliminate_piece(board, x, y):
	piece = board[y][x]
	board[y][x] = None
	if piece.name == ZONG:
		board = flip_flag_piece(board, piece.team)
	return board

'''
Flips the flag piece of a team so that it is publicly displayed
This happens when the ZONG of a team, its largest piece, is eliminated.
Input
	board :: 2D list = the full piece board of current game
	team :: Int in [0, 1] = the team whose flag piece must be displayed
Output :: board :: Updated board
'''
def flip_flag_piece(board, team):
	if team:
		row = BOARD_ROWS - 1
	else:
		row = 0
	for col in BASE_COLS:
		piece = board[row][col]
		if piece.name == FLAG:
			piece.do_display = True
			return board
	raise Exception("Did not find flag piece in the two bases in the board", board)
