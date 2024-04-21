from enum import Enum

class piece_identifier(Enum):
    white = 16
    black = 8
    none = 0
    king = 1
    pawn = 2
    knight = 3
    bishop = 4
    rook = 5
    queen = 6

print(piece_identifier['pawn'].value)

#hi