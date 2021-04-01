import pygame
from pygame.locals import *
from Pieces import Bishop
from Files import Color, WIDTH, HEIGHT
from Board import Board


class game:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = Board()
        self._running = False
        self._playerClicks = []

    def play(self):

        pygame.init()
        self._running = True

        screen = self.screen
        playerClicked = self._playerClicks
        board = self.board

        while self._running:

            self.board.draw(screen)

            for e in pygame.event.get():
                if e.type == QUIT:
                    self._running = False

                if e.type == MOUSEBUTTONDOWN:

                    if e.button == 1:
                        mx, my = e.pos
                        for square in board:
                            if square.rect.collidepoint(mx, my):
                                print(square, square.isSelected)
                                if square.isSelected:  # User already selected
                                    self.resetActions()
                                else:
                                    square.select()
                                    playerClicked.append(square)
                                if len(playerClicked) == 2:
                                    fromSq = playerClicked[0]
                                    toSq = playerClicked[1]

                                    try:
                                        piece = board.map.get(
                                            fromSq.location).currentPiece
                                        piece.moveToSquare(toSq)
                                        self.resetActions()
                                    except AttributeError:
                                        self.resetActions()

                        board.draw(screen)

            pygame.display.update()
            self.clock.tick(60)

    def resetActions(self):
        self.board.deselect()
        self._playerClicks = []


game = game()
game.play()
