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

def generateSlidingMoves(start_square, colour_to_move, moves, board):
    DIRECTION_OFFSETS =[8, -8, 1, -1, 7, 9, -9, -7]
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

def generateKnightMoves(start_square, colour_to_move, moves, board):
    knight_offsets = [15, 17, -17, -15, 10, 6, -6, -10] # Knight movement offsets
    for offset_index in range(8): #iterate over every directional offset
        target_square = start_square + knight_offsets[offset_index]
        if (target_square >=0) and (target_square <= 63) and (abs(target_square%8 - start_square%8) <= 2) and (board[target_square] & 24 != colour_to_move): 
            #Check whether our target square:
            #   1. Exists on the board
            #   2. Is a valid square to move to
            #   3. Doesn't have a friendly piece on it
            moves.append([start_square, target_square])
        else:
            continue

def generatePawnMoves(start_square, colour_to_move, moves, moves_log, board): #NEEDS OPTIMISING 
    pawn_offsets = [16, 8, 9, 7] #Negatives for black
    power = 0 if colour_to_move == 16 else 1 # Power exists for negative values for black later
    pawn_offset_start = 0 if ((start_square//8 == 1 and power == 0) or (start_square// 8 == 6 and power == 1)) else 1 # offset 16 exists for double pawn push
    pawn_offset_end = 4
    valid = False
    for pawn_offset_index in range(pawn_offset_start, pawn_offset_end):
        target_square = start_square + (-1)**power * pawn_offsets[pawn_offset_index]
        if (target_square >=0) and (target_square <= 63) and (abs(target_square%8 - start_square%8) <= 1): # check if target is a valid square
            if pawn_offsets[pawn_offset_index] %2 == 1 and board[target_square] & 24 != colour_to_move and board[target_square] != 0: #If we're checking diagonally, the target is of opposite colour and isn't empty
                valid = True
            elif pawn_offsets[pawn_offset_index] %2 == 0 and board[target_square] == 0: # Checking if target ahead is empty
                valid = True
            elif (pawn_offsets[pawn_offset_index] %2 == 1 # Checking for En passant diagonally
                    and len(moves_log)!=0#new addition, make sure to document
                    and abs(moves_log[-1][0] - moves_log[-1][1]) == 16 #Last move must've been a double push
                    and board[moves_log[-1][1]] & 7 == 2 #The double push was a pawn
                    and board[moves_log[-1][1]] &24 != colour_to_move #The pushed pawn is of the opposite colour (shouldn't be necessary)
                    and target_square == moves_log[-1][1] + 8 * (-1)**power): #The target square is the square behind the pushed pawn
                valid = True
            if valid and ((target_square // 8 == 7 and colour_to_move == 16) or (target_square // 8 == 0 and colour_to_move == 8)):
                #Promotions are recorded with a 3rd value in moves which is the identity of the new piece
                moves.append([start_square, target_square, colour_to_move | pieceIdentifier["q"].value])
                moves.append([start_square, target_square, colour_to_move | pieceIdentifier["r"].value])
                moves.append([start_square, target_square, colour_to_move | pieceIdentifier["n"].value])
                moves.append([start_square, target_square, colour_to_move | pieceIdentifier["b"].value])
            elif valid: moves.append([start_square, target_square])
            valid = False 
        else:
            continue
def generateKingMoves(start_square, colour_to_move, moves, moves_log, castling_rights, board):
    DIRECTION_OFFSETS =[8, -8, 1, -1, 7, 9, -9, -7]
    opposing_colour = 8 if colour_to_move == 16 else 16
    opposing_king_square = board.index(opposing_colour+1)
    #CASTLING
    #Check castling rights first
    if colour_to_move == 16 and castling_rights & 12 > 0:
        #first need to check whether castling is still allowed
        for i in moves_log:
            if (4 in i):
                castling_rights = castling_rights & 3 #White loses castling rights because white king has moved
            if (0 in i):
                castling_rights  = castling_rights & 7#white loses queen side castling rights
            if (7 in i):
                castling_rights = castling_rights & 11#white loses king side castling rights
    elif colour_to_move == 8 and castling_rights & 3 > 0:
        for i in moves_log:
            if (60 in i):
                castling_rights = castling_rights & 12 #black loses castling rights because black king has moved
            if (56 in i):
                castling_rights  = castling_rights & 13#black loses queen side castling rights 
            if (63 in i):
                castling_rights = castling_rights & 14#black loses king side castling rights
    #Now that castling rights are updated, we should check if castling is allowed given the current gameboard
    #requires an "under attack" function...
    #check for castling in game by looking for king moving 2 squares, if so then rook must move too (target square - start sqaure, if +ve then k, else q)
    if colour_to_move ==16 and castling_rights &12 >0 and not underAttack(16, 4, moves_log, board):
        if (castling_rights & 8 == 8 
            and not underAttack(16, 3, moves_log, board)
            and not underAttack(16, 2, moves_log, board)
            and board[3] == 0
            and board[2] == 0
            and board[1] == 0):
            moves.append([start_square, 2])
        if (castling_rights & 4 == 4 
            and not underAttack(16, 5, moves_log, board)
            and not underAttack(16, 6, moves_log, board)
            and board[5] == 0
            and board[6] == 0):
            moves.append([start_square, 6])
    elif colour_to_move == 8 and castling_rights &3 >0 and not underAttack(8, 60, moves_log, board):
        if (castling_rights &2 == 2 
            and not underAttack(8, 59, moves_log, board) 
            and not underAttack(8, 58, moves_log, board)
            and board[59] == 0
            and board[58] == 0
            and board[57] == 0):
            moves.append([start_square, 58])
        if (castling_rights & 1 == 1 
            and not underAttack(8, 61, moves_log, board) 
            and not underAttack(8, 62 ,moves_log, board)
            and board[61] == 0
            and board[62] == 0):
            moves.append([start_square, 62])
    #check non-castling moves
    for direction_offset in DIRECTION_OFFSETS:
        target_square = start_square + direction_offset
        if (target_square >=0) and (target_square <= 63) and (abs(target_square%8 - start_square%8) <= 1) and (board[target_square] & 24 != colour_to_move) and ((opposing_king_square-target_square) not in DIRECTION_OFFSETS):
            #Last condition checks for a king within another block in that direction for the opponent's king, if there is one, the if condition is not met
            moves.append([start_square, target_square])
        else:
            continue

def underAttack(colour_to_move, start_square, moves_log, board):
    other_colour = colour_to_move^24
    new_moves = []
    new_moves = generatePseudoLegalMoves(other_colour, 0, moves_log, board)#we don't want to generate castling moves or we may end up in a recursive loop 
    for move in new_moves:
        if start_square in move:
            return True
    return False

def generatePseudoLegalMoves(colour_to_move, castling_rights, moves_log, board):
    moves=[]
    for start_square in range(len(board)):
        start_square_piece = board[start_square]
        if start_square_piece & 24 == colour_to_move: #Check its the correct colour
            if start_square_piece & 7 == 1: # Check if its a king
                generateKingMoves(start_square, colour_to_move, moves, moves_log, castling_rights, board)
            elif start_square_piece & 4 == 4: # Check whether its a sliding piece
                generateSlidingMoves(start_square,colour_to_move, moves, board)
            elif start_square_piece & 7 == 3:#Check whether its a knight
                generateKnightMoves(start_square, colour_to_move, moves, board)
            else:
                generatePawnMoves(start_square, colour_to_move, moves, moves_log, board)
    return moves

def generateLegalMoves(colour_to_move, castling_rights, moves_log, board):
    all_moves = generatePseudoLegalMoves(colour_to_move, castling_rights, moves_log, board)
    if underAttack(colour_to_move, board.index(colour_to_move+1), moves_log, board):
        moves_to_stop_check = []
        for move in all_moves:
            moves_log_copy= moves_log[:]
            board_copy= board[:]
            board_copy[move[1]] = board_copy[move[0]]
            board_copy[move[0]] = 0
            king_square = board_copy.index(colour_to_move+1)
            moves_log_copy.append(move)
            if not underAttack(colour_to_move, king_square, moves_log_copy, board_copy):
                moves_to_stop_check.append(move)
        return moves_to_stop_check
    else:
        return all_moves

#TEMP GAME STATE VARIABLES
colour_to_move = 16 #8 for black, 16 for white
moves_log = []
castling_rights = 15 #4 bits, first 2 bits for white for castling rights q and k in that order, second 2 bits for black. 0 = no castling, 1 = castling allowed
board = setBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

print(generateLegalMoves(colour_to_move, castling_rights, moves_log, board))
#castling is recorded as [king square, k/q] depending on where castle occurs.