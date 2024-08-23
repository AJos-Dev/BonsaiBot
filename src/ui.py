import pygame
import moves

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

def setPieces(screen, board):
    for square_index in range(len(board)):
        if board[square_index] == 0:
            continue
        else:
            path = "pieces/{piece_identifier}.png".format(piece_identifier = board[square_index])
            piece_image = pygame.image.load(path)
            screen.blit(piece_image, position_lookup[square_index])

def main():
    screen = pygame.display.set_mode((1024, 768))
    clock = pygame.time.Clock()
    chessboard_surf = createBoard()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
        screen.fill(pygame.Color('black'))
        screen.blit(chessboard_surf, OFFSET)
        setPieces(screen, board)
        pygame.display.flip()
        clock.tick(60)

board = [moves.pieceIdentifier["none"].value] * 64
board = moves.setBoard("5k1b/2P5/8/4q3/8/8/8/2KR4", board)

TILESIZE = 64
OFFSET = (256, 128)

position_lookup = positionLookup(True)
main()