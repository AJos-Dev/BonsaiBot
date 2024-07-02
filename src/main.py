from enum import Enum

class pieceIdentifier(Enum):
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
    
board = [pieceIdentifier['none'].value] * 64 # Initialized with the 'none' piece and set the length to 64

def setBoard(FEN_board: str):
    gameboard_index = 0

    fen_to_string = {"k": pieceIdentifier["k"].value,
                     "p": pieceIdentifier["p"].value,
                     "n": pieceIdentifier["n"].value,
                     "b": pieceIdentifier["b"].value,
                     "r": pieceIdentifier["r"].value,
                     "q": pieceIdentifier["q"].value,
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
            board[gameboard_index] = fen_to_string[i.lower()] | pieceIdentifier["white"].value
        else: # By elimination, its lowercase and therefore black
            board[gameboard_index] = fen_to_string[i] | pieceIdentifier["black"].value
        gameboard_index += 1

    #REVERSE BOARD - from 0 and 64 being TL and BR to BL and TR
    temp_board = []
    for i in range(0, 72, 8):
        temp_board.append(board[i-8: i])
    temp_board = temp_board[::-1]
    another_temp = []
    for rank in temp_board:
        another_temp.extend(rank)
    return another_temp
board = setBoard("8/N7/2Q5/8/8/8/8/8")
print(board)
#HUGE ISSUE HERE: setBoard sets the pieces from bottom left to top right when FEN notation is carried out from top left to bottom right

#print(board)

#no of squares to edge
def squaresToEdgeCount():
    squares_to_edge = []
    for rank in range(8):
        for file in range(8):
            North = 7-rank
            South = rank
            East = 7-file
            West = file
            N_W = min(North, West)
            N_E = min(North, East)
            S_W = min(South, West)
            S_E = min(South, East)
            squares_to_edge.append([North, South, East, West, N_W, N_E, S_W, S_E])
    return squares_to_edge
squares_to_edge = squaresToEdgeCount()
#print(squares_to_edge)

DIRECTION_OFFSETS =[8, -8, 1, -1, 7, 9, -9, -7]
colour_to_move = 16
moves = [] #2d array storing all possible start and end square 

def generateSlidingMoves(start_square):
    direction_offset_start = 4 if board[start_square] & 7 == 4 else 0 # More bit manipulation to check piece types
    direction_offset_end = 4 if board[start_square] & 7 == 5 else 8
    for current_direction_index in range(direction_offset_start,  direction_offset_end):#Iterate through relevant directions dictated by boundaries set above
        # Iterate over every square in that direction where the target square is i times the offset (e.g. from square 0 in the N direction, we add multiples of 8)
        for i in range(1, squares_to_edge[start_square][current_direction_index]+1): 
            target_square = start_square + i* DIRECTION_OFFSETS[current_direction_index]
            if board[target_square] & 24 == colour_to_move: # If target square is a friendly...
                break #...leave loop immedietly
            moves.append([start_square, target_square]) #As we continue onwards, we know it can be added to the list of moves
            if board[target_square] != 0: #If the target square has passed the criteria above and is not empty, by elimination it must be of the other colour
                break #in which case we stop iterating over this loop

def generateKnightMoves(start_square):
    knight_offsets = [15, 17, -17, -15, 10, 6, -6, -10]
    for offset_index in range(8):
        target_square = start_square + knight_offsets[offset_index]
        if (target_square >=0) and (target_square <= 63) and (abs(target_square%8 - start_square%8) <= 2) and (board[target_square] & 24 != colour_to_move):    
            moves.append([start_square, target_square])
        else:
            continue

def generatePawnMoves(start_square):
        pawn_offsets = [16, 8, 9, 7, -16, -8, -7, -9]
        if (board[start_square] // 8 == 1) and (colour_to_move == 16):
            pawn_offset_start = 0
            pawn_offset_end = 4
        elif (board[start_square] // 8 != 1) and (colour_to_move == 16):
            pawn_offset_start = 1
            pawn_offset_end = 4
        elif (board[start_square] // 8 == 6) and (colour_to_move == 8):
            pawn_offset_start = 4
            pawn_offset_end = 8
        elif (board[start_square] // 8 != 1) and (colour_to_move == 8):
            pawn_offset_start = 5
            pawn_offset_end = 8
        for pawn_offset_index in range(pawn_offset_start, pawn_offset_end):
            target_square = start_square + pawn_offsets[pawn_offset_index]
            if board[target_square] & 24 == colour_to_move:
                

def generate_moves():
    for start_square in range(len(board)):
        start_square_piece = board[start_square]
        if start_square_piece & 24 == colour_to_move: #Check its the correct colour
            if start_square_piece & 4 == 4: # Check whether its a sliding piece
                generateSlidingMoves(start_square)
            elif start_square_piece & 3 == 3:#Check whether its a knight
                generateKnightMoves(start_square)

generate_moves()
print(moves)
#ALL CURRENT CONVENTION IS IF PLAYER IS PLAYING WHITE (BLACK ON THE OTHER END)