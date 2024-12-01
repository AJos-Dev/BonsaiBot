import pygame
import moves
import random
import engine

pygame.init()
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
            tile = pygame.Rect(file * TILESIZE, rank * TILESIZE, TILESIZE, TILESIZE) #create a tile f or every row and rank
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

button_font = pygame.font.Font(None, 25)
class Button:
    # Button class: initializes the button with position, text, font, color, and callback function
    def __init__(self, text, position, size, piece):
        self.rect = pygame.Rect(position, size)
        self.text = text
        self.piece = piece
        self.fonts = button_font
        self.color = (100, 100, 100)

    def draw(self, surface):
        # This draws the buttons onto the display
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = self.fonts.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

def main():
    moves_log=[]
    colour_to_play = 16
    castling_rights = 15
    board = [moves.pieceIdentifier["none"].value] * 64
    board = moves.setBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", board)
    current_legal_moves= moves.generateLegalMoves(colour_to_play, castling_rights, moves_log, board)

    selected_piece = None
    screen = pygame.display.set_mode((1024, 768))
    clock = pygame.time.Clock()
    chessboard_surf = createBoard()
    drag = False
    setPieces(board)
    red_squares=[]
    pawnPromotionMenu = False
    while True:
        screen.fill(pygame.Color('black'))
        events = pygame.event.get()
        if pawnPromotionMenu == True:
            q_button = Button("Queen", (50, 10), (65, 55), moves.pieceIdentifier["q"].value)
            n_button = Button("Knight", (50, 70), (65, 55), moves.pieceIdentifier["n"].value)
            r_button = Button("Rook", (50, 130), (65, 55), moves.pieceIdentifier["r"].value)
            b_button = Button("Bishop", (50, 190), (65, 55), moves.pieceIdentifier["b"].value)
            q_button.draw(screen)
            n_button.draw(screen)
            r_button.draw(screen)
            b_button.draw(screen)
            buttons_list = [q_button, n_button, r_button, b_button]
        if colour_to_play == 8:
            move_to_play = engine.Search(3, board, colour_to_play, moves_log, castling_rights)
            for piece in pieces_group:
                if piece.getSquare() == move_to_play[0]:
                    selected_piece = piece
                elif piece.getSquare() == move_to_play[1]:
                    pieces_group.remove(piece)
            #REPETITION 1
            selected_piece.setPosition(position_lookup[move_to_play[1]])
            selected_piece.setSquare(move_to_play[1])
            board[move_to_play[1]] = board[move_to_play[0]]
            board[move_to_play[0]] = moves.pieceIdentifier["none"].value
            moves_log.append(move_to_play)
            colour_to_play ^= 24
            current_legal_moves = moves.generateLegalMoves(colour_to_play, castling_rights, moves_log, board)
            if len(current_legal_moves) == 0: #No moves to play indicates a checkmate or stalemate
                king_square = board.index(colour_to_play+1)
                if moves.underAttack(colour_to_play, king_square, moves_log, board):
                    print("Checkmate", colour_to_play^24, "wins!")
                else:
                    print("Stalemate!")
                exit()
            #ENDS HERE
        for event in events:
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for piece in pieces_group:
                    if piece.rect.collidepoint(event.pos) and not pawnPromotionMenu:
                        selected_piece = piece
                        old_square = selected_piece.getSquare()
                        drag = True
                    elif pawnPromotionMenu:
                        for button in buttons_list:
                            if button.rect.collidepoint(event.pos):
                                moves_log[-1].append(colour_to_play^24|button.piece)
                                selected_piece.setPieceIdentifier(button.piece | colour_to_play^24)
                                pawnPromotionMenu = False
                                board[moves_log[-1][1]] = moves_log[-1][2]
            elif drag and not pawnPromotionMenu:
                for move in current_legal_moves:
                    if move[0] == selected_piece.getSquare():
                        red_squares.append(move[1])
                mouse_x, mouse_y = event.pos
                mouse_x -= 25
                mouse_y -= 32
                mouse_pos = mouse_x, mouse_y
                selected_piece.setPosition(mouse_pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    red_squares = []
                    move_to_play = [selected_piece.getSquare(), squareUnderMouse(white_perspective)[1]* 8 + squareUnderMouse(white_perspective)[0]]
                    if move_to_play in [i[:2] for i in current_legal_moves]:
                        for move in current_legal_moves:
                            if len(move) == 3 and move[:2] == move_to_play:
                                pawnPromotionMenu = True
                                break
                        #check whether the piece just moved was a king
                        if selected_piece.getPieceIdentifier()&7 == moves.pieceIdentifier["k"].value:
                            #if it is a king, did it move 2 squares (was it a castle)?
                            if move_to_play[1]-move_to_play[0] == 2: #was it a kingside castle?
                                for piece in pieces_group:
                                    if piece.getSquare() == move_to_play[1] + 1:
                                        board[move_to_play[1]+1] = moves.pieceIdentifier["none"].value
                                        board[move_to_play[1]-1] = piece.getPieceIdentifier()
                                        piece.setPosition(position_lookup[move_to_play[1]-1])
                                        piece.setSquare(move_to_play[1]-1)
                                        moves_log.append([move_to_play[1]+1, move_to_play[1]-1])
                            elif move_to_play[1]-move_to_play[0] == -2: #was it a queenside castle?
                                for piece in pieces_group:
                                    if piece.getSquare() == move_to_play[1] - 2:
                                        board[move_to_play[1]-2] = moves.pieceIdentifier["none"].value
                                        board[move_to_play[1]+1] = piece.getPieceIdentifier()
                                        piece.setPosition(position_lookup[move_to_play[1]+1])
                                        piece.setSquare(move_to_play[1]+1)
                                        moves_log.append([move_to_play[1]-2, move_to_play[1]+1])
                        #remove the opposing piece in the target square
                        for piece in pieces_group:
                            if piece.getSquare() == move_to_play[1]:
                                pieces_group.remove(piece)
                        #update position on the board with the new move the pieces
                        #TURN INTO FUNCTION
                        selected_piece.setPosition(position_lookup[move_to_play[1]])
                        selected_piece.setSquare(move_to_play[1])
                        board[move_to_play[1]] = board[move_to_play[0]]
                        board[move_to_play[0]] = moves.pieceIdentifier["none"].value#replace old square with an empty piece
                        moves_log.append(move_to_play) #add move to move log
                        colour_to_play ^= 24 #alternate between colours to play
                        current_legal_moves = moves.generateLegalMoves(colour_to_play, castling_rights, moves_log, board)
                        if len(current_legal_moves) == 0: #No moves to play indicates a checkmate or stalemate
                            king_square = board.index(colour_to_play+1)
                            if moves.underAttack(colour_to_play, king_square, moves_log, board):
                                print("Checkmate", colour_to_play^24, "wins!")
                            else:
                                print("Stalemate!")
                            exit()
                        #TURN INTO FUNCTION ENDS HERE
                    else:   
                        selected_piece.setPosition(position_lookup[old_square])
                    drag = False
        screen.blit(chessboard_surf, OFFSET)
        pieces_group.draw(screen)
        for square in red_squares:
            pygame.draw.circle(screen, (255, 0, 0), (position_lookup[square][0] + 25, position_lookup[square][1]+27), 5)
        pygame.display.flip()
        clock.tick(60)

pieces_group=pygame.sprite.Group()

white_perspective = True
TILESIZE = 64
OFFSET = (256, 128)

position_lookup = positionLookup(white_perspective)
main()