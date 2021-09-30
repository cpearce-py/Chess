from contextlib import contextmanager

import pygame
from constants import Color

from player import Player
from fen import PositionInfo, load_from_fen, START_FEN
from move import MoveHandler, Move

@contextmanager
def ignore(*exceptions, func=None):
    try:
        yield
    except exceptions as e:
        print(e)
        func()

_load_position = load_from_fen(START_FEN)

class GameHandler():

    def __init__(self, board, load_position: PositionInfo=_load_position):
        self.clicks =  []
        self.board = board
        self.board.init(load_position)

        whiteToMove = load_position.whiteToMove

        self.turn = Color.LIGHT if whiteToMove else Color.DARK

        self.players = {Color.LIGHT: Player(Color.LIGHT, board),
                        Color.DARK: Player(Color.DARK, board)}
        self.curr_player = self.players.get(self.turn)

        self.move_handler = MoveHandler(board, whiteToMove=whiteToMove)
        self.move_handler.generate_moves()
        self.move_handler.highlight_attacked()

    def handle_events(self, event):
        self.check_quit_event(event)
        self.check_mouse_click_event(event)

    def check_quit_event(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.K_ESCAPE):
            pygame.quit()

    def check_mouse_click_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            square = self.hitSquare(event.pos)

            if not square or square.isSelected:
                self.reset_clicks()
                return

            if len(self.clicks) == 0:
                square.select()

            self.clicks.append(square)

            if len(self.clicks) == 2:
                fromSq, toSq = self.clicks
                if not fromSq.isOccupied:
                    self.reset_clicks()
                    return
                move = Move(fromSq, toSq)
                self.move_handler.try_move(move)
                self.clicks = []

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if square := self.hitSquare(event.pos):
                square.isAttacked = not square.isAttacked

    def reset_clicks(self):
        self.board.deselect()
        self.clicks = []

    def hitSquare(self, pos):
        for square in self.board:
            if square.rect.collidepoint(pos):
                return square
