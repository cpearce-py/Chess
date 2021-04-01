import pygame
from pygame.locals import *
from Pieces import Bishop
from Files import Color, WIDTH, HEIGHT
from Board import Board

pygame.init()

clock = pygame.time.Clock()

piece = Bishop(Color.LIGHT)


screen = pygame.display.set_mode((WIDTH, HEIGHT))


board = Board()
board.draw(screen)

pieces_grp = pygame.sprite.Group()
pieces_grp.add(piece)

running = True
clicking = False

while running:

    board.draw(screen)
    pieces_grp.draw(screen)

    mx, my = pygame.mouse.get_pos()

    # Button events
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                clicking = True
                for square in board:
                    if square.rect.collidepoint(mx, my):
                        for piece in pieces_grp:
                            piece.moveToSquare(square)

                pieces_grp.update()

        if e.type == MOUSEBUTTONUP:
            if e.button == 1:
                clicking = False

    pygame.display.update()
    clock.tick(60)
