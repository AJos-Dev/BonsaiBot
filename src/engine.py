import moves

colour_to_move = 16
board = [moves.pieceIdentifier["none"].value] * 64
board = moves.setBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", board)
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

#probably because castling is handled weirdly