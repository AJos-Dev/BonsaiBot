import moves
pawnValue = 100
knightValue = 300
bishopValue = 300
rookValue = 500
queenValue = 900

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

board = [moves.pieceIdentifier["none"].value] * 64
board= moves.setBoard("3rk3/1Pr5/P7/8/5p2/5Pp1/2R1B2p/3K1N2", board)
print(Evaluate(board, 8))

def Search(depth, board, colour_to_move, moves_log, castling_rights):
    if depth == 3:
        evaluated_moves = []
    if depth == 0:
        return Evaluate(board, colour_to_move)
    current_moves = moves.generateLegalMoves(colour_to_move, castling_rights, moves_log, board)
    if len(current_moves) == 0:
        king_square = board.index(colour_to_move+1)
        if moves.underAttack(colour_to_move, king_square, moves_log, board):
            return float('-inf')
        return 0
    best_evaluation = float("-inf")
    for move in current_moves:
        #Need to check for pawn promotions, look at ui.py for implementation
        #meed to check for castling as well 
        moves_log_copy= moves_log[:]
        board_copy= board[:]
        board_copy[move[1]] = board_copy[move[0]]
        board_copy[move[0]] = 0
        moves_log_copy.append(move)
        colour_to_move_copy = colour_to_move ^ 24
        evaluation = -Search(depth-1, board_copy, colour_to_move_copy, moves_log_copy, castling_rights)
        if depth == 3:
            evaluated_moves.append(evaluation)
        best_evaluation = max(evaluation, best_evaluation)
    if depth == 3:
        return current_moves[evaluated_moves.index(best_evaluation)]
    return best_evaluation
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