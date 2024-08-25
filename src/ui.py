import pygame
import moves
import random

class Piece(pygame.sprite.Sprite):
    def __init__(self, square, board):
        super().__init__()
        self.square = square
        self.piece_identifier = board[self.square]
        self.path = "pieces/{piece_identifier}.png".format(piece_identifier = board[self.square])
        self.image = pygame.image.load(self.path)
        self.position =  position_lookup[self.square]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
    def getPieceIdentifier(self):
        return self.piece_identifier
    def getSquare(self):
        return self.square
    def setSquare(self, square):
        self.square = square
        self.position = position_lookup[self.square]
        self.rect = self.image.get_rect()
        self.rect.topleft=self.position
    def setPosition(self, position):
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
    def setPieceIdentifier(self, piece_identifier):
        self.piece_identifier = piece_identifier
        self.path = "pieces/{piece_identifier}.png".format(piece_identifier = self.piece_identifier)
        self.image = pygame.image.load(self.path)

def createBoard():
    chessboard_surf = pygame.Surface((TILESIZE * 8, TILESIZE * 8))#create chessboard surface
    white = True
    for rank in range(8):
        for file in range(8):
            tile = pygame.Rect(file * TILESIZE, rank * TILESIZE, TILESIZE, TILESIZE) #create a tile for every row and rank
            pygame.draw.rect(chessboard_surf, pygame.Color('blanchedalmond' if white else 'burlywood4'), tile) #draw it, alternating black/white
            white= not white
        white= not white
    return chessboard_surf #return the surface

def positionLookup(white_perspective):
    position_lookup = []
    if white_perspective:
        for i in range(64):
            position = [OFFSET[0] + i % 8 * TILESIZE - 25 + TILESIZE/2, OFFSET[1] + (7-(i//8)) * TILESIZE +5]
            position_lookup.append(position)
        return position_lookup
    else:
        for i in range(64):
            position = [OFFSET[0] + (7-(i%8)) * TILESIZE-25+ TILESIZE/2, OFFSET[1] + i//8 * TILESIZE + 5]
            position_lookup.append(position)
        return position_lookup
    
def squareUnderMouse(white_perspective):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - OFFSET
    file, rank = [int(v//TILESIZE) for v in mouse_pos]
    if white_perspective: return file, 7-rank
    else: return 7-file, rank

def setPieces(board):
    for square_index in range(len(board)):
        if board[square_index] == 0:
            continue
        else:
            piece = Piece(square_index, board)
            pieces_group.add(piece)

def main():
    moves_log=[]
    colour_to_play = 8
    castling_rights = 15
    board = [moves.pieceIdentifier["none"].value] * 64
    board = moves.setBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", board)
    current_legal_moves= moves.generateLegalMoves(colour_to_play, castling_rights, moves_log, board)
    print(current_legal_moves)

    selected_piece = None
    screen = pygame.display.set_mode((1024, 768))
    clock = pygame.time.Clock()
    chessboard_surf = createBoard()
    drag = False
    setPieces(board)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for piece in pieces_group:
                    if piece.rect.collidepoint(event.pos):
                        selected_piece = piece
                        old_square = selected_piece.getSquare()
                        drag = True
            elif drag:
                mouse_x, mouse_y = event.pos
                mouse_x -= 25
                mouse_y -= 32
                mouse_pos = mouse_x, mouse_y
                selected_piece.setPosition(mouse_pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    move_to_play = [selected_piece.getSquare(), squareUnderMouse(white_perspective)[1]* 8 + squareUnderMouse(white_perspective)[0]]
                    if move_to_play in current_legal_moves:
                        for piece in pieces_group:
                            if piece.getSquare() == move_to_play[1]:
                                pieces_group.remove(piece)
                        selected_piece.setPosition(position_lookup[move_to_play[1]])
                        selected_piece.setSquare(move_to_play[1])
                        board[move_to_play[1]] = board[move_to_play[0]]
                        board[move_to_play[0]] = moves.pieceIdentifier["none"].value
                        moves_log.append(move_to_play)
                        colour_to_play ^= 24
                        current_legal_moves = moves.generateLegalMoves(colour_to_play, castling_rights, moves_log, board)
                        if len(current_legal_moves) == 0:
                            print("Checkmate", colour_to_play^24, "wins!")
                            exit()
                    else:
                        selected_piece.setPosition(position_lookup[old_square])
                    drag = False
        screen.fill(pygame.Color('black'))
        screen.blit(chessboard_surf, OFFSET)
        pieces_group.draw(screen)
        pygame.display.flip()
        clock.tick(60)


pieces_group=pygame.sprite.Group()


white_perspective = False
TILESIZE = 64
OFFSET = (256, 128)

position_lookup = positionLookup(white_perspective)
main()

#Pinned pieces no workey :( :()