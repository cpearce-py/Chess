from contextlib import contextmanager

import pygame
from constants import Files, Color

from player import Player
from fen import PositionInfo, load_from_fen, START_FEN, FEN1
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
        self.turn = Color.LIGHT if load_position.whiteToMove else Color.DARK
        self.players = {Color.LIGHT: Player(Color.LIGHT, self.board),
                        Color.DARK: Player(Color.DARK, self.board)}
        self.curr_player = self.players.get(self.turn)
        self.move_handler = MoveHandler(board)
        self.move_handler.generate_moves(self.turn)

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
                if not square:
                    self.resetActions()
                    return

                if square.isSelected:
                    self.resetActions()
                    return

                if len(self.clicks) == 0:
                    square.select()

                self.clicks.append(square)

                if len(self.clicks) == 2:
                    fromSq, toSq = self.clicks
                    move = Move(fromSq.location, toSq.location)

                    with ignore(AttributeError, ValueError, func=self.resetActions):
                        piece = board.get_piece_from_loc(fromSq.location)
                        if piece.color != self.turn:
                            self.resetActions()
                            return
                        possibleMoves = piece.getValidMoves(self.board)
                        piece.moveToSquare(toSq, possibleMoves, self.board)
                        self.turn = Color.DARK if self.turn == Color.LIGHT else Color.LIGHT
                        self.move_handler
                        self.endTurn(self.turn)
                        self.resetActions()

    def hitSquare(self, pos):
        for square in self.board:
            if square.rect.collidepoint(pos):
                return square

    def endTurn(self, player):
        self.board.deselect()
        self.clicks = []
        self.curr_player = self.players.get(player)

    def resetActions(self):
        self.board.deselect()
        self.clicks = []
