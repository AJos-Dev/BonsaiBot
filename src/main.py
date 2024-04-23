from enum import Enum

class piece_identifier(Enum):
    white = 16
    black = 8
    none = 0
    k = 1 # king
    p = 2 # pawn
    n = 3 # knight
    b = 4 # bishop
    r = 5 # rook
    q = 6 # queen

#turn pieces into letters for easier conversion with FEN
board = [piece_identifier['none'].value] * 64

def set_board(FEN_board: str):
    FEN_fields = FEN_board.split(" ")
    gameboard_index = 0
    for i in FEN_fields[0]:
        print(i)
        if ord(i) == 47: # a '/' in FEN must just be ignored
            continue
        elif ord(i) <= 57: # a number in FEN needs to jump that many spaces 
            gameboard_index += int(i)
        elif ord(i) <= 90: # a capital letter in FEN corresponds to a white piece
            #board[gameboard_index] = piece_identifier[i.lower()].value |  piece_identifier['white'].value 
            board[gameboard_index] = i
        else: #vice versa for a black piece
            #board[gameboard_index] = piece_identifier[i.lower()].value |  piece_identifier['black'].value
            board[gameboard_index] = i


set_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
print(board)