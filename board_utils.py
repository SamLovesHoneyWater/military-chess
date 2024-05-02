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

HALF_TERRAIN = [
                [RAIL, RAIL, RAIL, RAIL, RAIL],
                [RAIL, LAKE, LAND, LAKE, RAIL],
                [RAIL, LAND, LAKE, LAND, RAIL],
                [RAIL, LAKE, LAND, LAKE, RAIL],
                [RAIL, RAIL, RAIL, RAIL, RAIL],
                [LAND, BASE, LAND, BASE, LAND]
            ]

pretty_print(HALF_TERRAIN)

'''
Compare two pieces
Input
    subject :: Piece = the piece whose outcome we are interested in
    target :: Piece = the piece being compared against
Output :: Int in [0,2] where 0 means subject lost, 1 means subject won,and 2 means both sides
are destroyed.
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
        return 1
    elif rank_subject == rank_target:  # Equal force
        return 2
    elif rank_subject > rank_target:  # Won
        return 1
    else:  # Lost
        return 0
