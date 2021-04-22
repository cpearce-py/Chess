import pygame
from Files import Color

class EventHandler():
    def __init__(self, board, turn=Color.LIGHT):
        self.clicks =  []
        self.board = board
        self.turn = turn

    def handle_events(self, event):
        self.check_quit_event(event)
        self.check_mouse_click_event(event)

    def check_quit_event(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.K_ESCAPE):
            pygame.quit()

    def check_mouse_click_event(self, event):
        board = self.board
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos
                square = self.hitSquare(event.pos)
                if square:
                    if square.isSelected:
                        self.resetActions()
                        return

                    if len(self.clicks) == 0:
                        square.select()

                    self.clicks.append(square)

                    if len(self.clicks) == 2:
                        fromSq = self.clicks[0]
                        toSq = self.clicks[1]

                        try:
                            piece = board.map.get(fromSq.location).currentPiece
                            if piece.color == self.turn:
                                possibleMoves = piece.getValidMoves(self.board)
                                piece.moveToSquare(toSq, possibleMoves, self.board)
                                self.turn = Color.DARK if self.turn == Color.LIGHT else Color.LIGHT
                            self.resetActions()
                        except (AttributeError, ValueError) as e:
                            print(e)
                            self.resetActions()

    def hitSquare(self, pos):
        for square in self.board:
            if square.rect.collidepoint(pos):
                return square

    def resetActions(self):
        self.board.deselect()
        self.clicks = []
