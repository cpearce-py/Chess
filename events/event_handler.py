import pygame
from constants import Files, Color
from contextlib import contextmanager

@contextmanager
def ignore(*exceptions, func=None):
    try:
        yield
    except exceptions as e:
        print(e)
        func()

class BaseHandler():
    def __init__(self):
        pass

    def on_mbutton_down(self, event):
        pass

class MenuHandler(BaseHandler):
    def __init__(self):
        pass


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
                square = self.hitSquare(event.pos)
                if square:
                    if square.isSelected:
                        self.resetActions()
                        return

                    if len(self.clicks) == 0:
                        square.select()

                    self.clicks.append(square)

                    if len(self.clicks) == 2:
                        fromSq, toSq = self.clicks

                        with ignore(AttributeError, ValueError, func=self.resetActions):
                            piece = board.map.get(fromSq.location).currentPiece
                            if piece.color == self.turn:
                                possibleMoves = piece.getValidMoves(self.board)
                                piece.moveToSquare(toSq, possibleMoves, self.board)
                                self.turn = Color.DARK if self.turn == Color.LIGHT else Color.LIGHT
                            self.resetActions()

    def hitSquare(self, pos):
        for square in self.board:
            if square.rect.collidepoint(pos):
                return square

    def resetActions(self):
        self.board.deselect()
        self.clicks = []
