import moves
pawnValue = 100
knightValue = 300
bishopValue = 300
rookValue = 500
queenValue = 900
max_depth = 3

def countMaterial(board, colour):
    material = 0
    for square in board:
        current_piece = square & 7
        if square & 24 == colour:
            if current_piece == 2:
                material += pawnValue
            elif current_piece == 3:
                material += knightValue
            elif current_piece == 4:
                material += bishopValue
            elif current_piece == 5:
                material += rookValue
            elif current_piece == 6:
                material += queenValue
    return material

def Evaluate(board, colour):
    whiteEval = countMaterial(board, 16)
    blackEval = countMaterial(board, 8)
    perspective = -1 if colour == 8 else 1
    evaluation = whiteEval - blackEval
    return perspective * evaluation

#board = [moves.pieceIdentifier["none"].value] * 64
#board= moves.setBoard("3rk3/1Pr5/P7/8/5p2/5Pp1/2R1B2p/3K1N2", board)
#print(Evaluate(board, 8))

def Search(depth, board, colour_to_move, moves_log, castling_rights):
    if depth == max_depth: #Will run at the start to create a list to store evaluations
        evaluated_moves = []
    if depth == 0: #For every end board (Leaf node), we run an evaluation to give the board a score
        return Evaluate(board, colour_to_move)
    #Now a list of moves that we can play must be generated
    current_moves = moves.generateLegalMoves(colour_to_move, castling_rights, moves_log, board) 
    if len(current_moves) == 0: # No legal moves indicates checkmate or stalemate
        king_square = board.index(colour_to_move+1)
        if moves.underAttack(colour_to_move, king_square, moves_log, board): #we check if we're under attack
            return float('-inf')#If so, this is a theoretical checkmate, the worst outcome for us
        return 0 #Otherwise we have a stalemate, which is neutral but we'd rather not be in this situation
    best_evaluation = float("-inf") #This is so we can make any move which is better than checkmate
    for move in current_moves:
        #Need to check for pawn promotions, look at ui.py for implementation
        #need to check for castling as well
        moves_log_copy= moves_log[:]
        board_copy= board[:]
        #board_copy[move[1]] = board_copy[move[0]]##
        #board_copy[move[0]] = 0##
        #moves_log_copy.append(move)##
        if len(move) == 3: #handle pawn promotions
            board_copy[move[1]] = board_copy[move[2]]
        elif board[move[0]]&7 == moves.pieceIdentifier["k"].value:
            if move[1] - move[0] == 2:#check kingside castle
                piece_identifier = board_copy[move[1]+1] #if so, move the rook to its correct place
                board_copy[move[1]+1] = moves.pieceIdentifier["none"].value
                board_copy[move[1]-1] = piece_identifier
                moves_log.append([move[1]+1, move[1]-1])
            elif move[1] - move[0] == -2: #check queenside castle
                piece_identifier = board_copy[move[1]-2]
                board_copy[move[1]-2] = moves.pieceIdentifier["none"].value
                board_copy[move[1]+1] = piece_identifier
                moves_log.append([move[1]-2, move[1]+1])
            board_copy[move[1]] = board_copy[move[0]]
        else:
            board_copy[move[1]] = board_copy[move[0]]
        board_copy[move[0]] = 0

        moves_log_copy.append(move)
        colour_to_move_copy = colour_to_move ^ 24
        evaluation = -Search(depth-1, board_copy, colour_to_move_copy, moves_log_copy, castling_rights) #-ve is important as a move good for the opponent is bad for us, also returns the best evaluation for that subtree
        if depth == max_depth: #If we are at the max_depth of 3, it means we've just evaluated all the moves from one edge of the tree (an entire subtree)
            evaluated_moves.append(evaluation) #therefore we must add the evaluation to the evaluated moves list (1:1 correlation with current_moves)
        best_evaluation = max(evaluation, best_evaluation) #We also keep track of the best evaluation regardless
    if depth == max_depth: #After completing all the moves from the top of the tree, we return the *move* which we have tracked as best for us.
        return current_moves[evaluated_moves.index(best_evaluation)]
    return best_evaluation #Because we haven't completed all the moves, we simply return the best evaluation for this branch(to keep track of the best evaluated move to append to best_evaluation)
'''
colour_to_move = 16
board = [moves.pieceIdentifier["none"].value] * 64
board = moves.setBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", board)
print(countMaterial(board, 16))
moves_log = []
castling_rights = 0
def moveGenerationTest(depth):
    if depth == 0:
        return 1
    moves_list = moves.generateLegalMoves(colour_to_move if depth % 2==0 else colour_to_move^24, castling_rights, moves_log, board)
    numPositions = 0

    for move in moves_list:
        temp_1 = board[move[1]]
        temp_0 = board[move[0]]
        board[move[1]] = board[move[0]]
        board[move[0]] = 0
        moves_log.append(move)
        numPositions += moveGenerationTest(depth -1)
        board[move[1]] = temp_1
        board[move[0]] = temp_0
        moves_log.pop()
    return numPositions

print(moveGenerationTest(3))
'''
#probably because castling is handled weirdly