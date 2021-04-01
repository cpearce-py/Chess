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
        self.running = False
        self.playerClicked = []

    def play(self):

        pygame.init()
        self.running = True

        screen = self.screen
        playerClicked = self.playerClicked
        board = self.board

        while self.running:

            self.board.draw(screen)

            for e in pygame.event.get():
                if e.type == QUIT:
                    self.running = False

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
                                    self.playerClicked.append(square)

                                if len(self.playerClicked) == 2: # Second click
                                    fromSq = self.playerClicked[0]
                                    toSq = self.playerClicked[1]

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
        self.playerClicked = []


game = Game()
game.play()
