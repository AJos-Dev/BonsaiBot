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

#pieces => letters for easier conversion with FEN
    
board = [piece_identifier['none'].value] * 64 # Initialized with the 'none' piece and set the length to 64

def set_board(FEN_board: str):
    gameboard_index = 0

    fen_to_string = {"k": piece_identifier["k"].value,
                     "p": piece_identifier["p"].value,
                     "n": piece_identifier["n"].value,
                     "b": piece_identifier["b"].value,
                     "r": piece_identifier["r"].value,
                     "q": piece_identifier["q"].value,
                     }

    try:
        FEN_board = FEN_board.replace("/", "")
    except:
        raise Exception("Invalid data type")

    for i in FEN_board:
        if i.isdigit(): # Check its a digit...
            gameboard_index += int(i)-1
        elif i.lower() not in fen_to_string: # ... before we check whether its a letter in our dictionary
            raise Exception("Invalid character within FEN string")
        elif i.isupper(): #We know its in our dictionary, is it uppercase? If so then piece is white
            board[gameboard_index] = fen_to_string[i.lower()] | piece_identifier["white"].value
        else: # By elimination, its lowercase and therefore black
            board[gameboard_index] = fen_to_string[i] | piece_identifier["black"].value
        gameboard_index += 1

set_board("q7/6P1/1K6/2N5/6P1/8/5P2/1k6")
print(board)