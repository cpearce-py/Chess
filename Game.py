import pygame
from pygame.locals import *
from Pieces import Bishop
from Files import Color, WIDTH, HEIGHT
from Board import Board


class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = Board()
        self._running = False
        self._playerClicked = []

    def play(self):

        pygame.init()
        self._running = True

        screen = self.screen
        playerClicked = self._playerClicked
        board = self.board

        while self._running:

            self.board.draw(screen)

            for e in pygame.event.get():
                if e.type == QUIT:
                    self._running = False

                if e.type == MOUSEBUTTONDOWN:

                    if e.button == 1:
                        mx, my = e.pos
                        for square in self.board:
                            if square.rect.collidepoint(mx, my):
                                print(square, square.isSelected)
                                if square.isSelected:  # User already selected
                                    self.resetActions()
                                else:
                                    square.select()
                                    self._playerClicked.append(square)
                                if len(self._playerClicked) == 2:
                                    fromSq = self._playerClicked[0]
                                    toSq = self._playerClicked[1]

                                    try:
                                        piece = board.map.get(
                                            fromSq.location).currentPiece
                                        possibleMoves = piece.getValidMoves(
                                            board)
                                        piece.moveToSquare(toSq, possibleMoves)
                                        self.resetActions()
                                    except (AttributeError, ValueError) as e:
                                        print(e)
                                        self.resetActions()

                        board.draw(screen)

            pygame.display.update()
            self.clock.tick(60)

    def resetActions(self):
        self.board.deselect()
        self._playerClicked = []


game = Game()
game.play()
