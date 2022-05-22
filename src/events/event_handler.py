from __future__ import annotations
import sys
from typing import (
    TYPE_CHECKING,
    Tuple,
    Optional,
    cast,
)

import pygame

import move_generator as mg
from fen import START_FEN, PositionInfo, load_from_fen
from move import Flag, Move, MoveHandler

if TYPE_CHECKING:
    from board import Board
    from scenes.scenes import Scene
    from squares import Square

_load_position = load_from_fen(START_FEN)


class GameHandler:
    def __init__(
        self, board: Board, scene: Scene, load_position: PositionInfo = _load_position
    ):
        self.clicks = []
        self.board = board
        self.board.init(load_position)
        white_to_move = load_position.whiteToMove
        self.move_handler = MoveHandler(board, white_to_move=white_to_move)
        self.move_handler.generate_moves()
        self.move_generator = mg.MoveGenerator(board)
        self.move_generator.generate_moves()
        self._scene = scene

    def handle_events(self, event):
        self.check_quit_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_mouse_click_event(event)
        elif event.type == pygame.KEYDOWN:
            self.check_arrow_event(event)
        else:
            pass

    def check_quit_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def check_mouse_click_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            square = self.hitSquare(event.pos)

            if not square or square.isSelected:
                self.reset_clicks()
                return

            if len(self.clicks) == 0:
                square.select()

            self.clicks.append(square)

            if len(self.clicks) == 2:
                from_sq, to_sq = self.clicks
                if not from_sq.isOccupied:
                    self.reset_clicks()
                    return
                user_move = Move(from_sq, to_sq)
                if user_move in self.move_generator:
                    user_move = self.move_generator.get_move(user_move)
                    self.board.make_move(user_move)
                    self.end_turn()
                else:
                    self.reset_clicks()

                # This chunk of code is for testing promotion.

                # move = self.move_generator.get_move(user_move)
                # if user_move:
                #    self.move_handler.try_move(user_move)
                #    if user_move.flag == Flag.PROMOTE:
                #        colour_to_promote = user_move.toSq.piece.color
                #        self._scene.promote(colour_to_promote)
                #    self.end_turn()
                # else:
                #    self.reset_clicks()
                # if self.move_handler.try_move(user_move):
                #     self.end_turn()
                # else:
                #     self.reset_clicks()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if square := self.hitSquare(event.pos):
                square.isAttacked = not square.isAttacked

    def check_arrow_event(self, event):
        if event.key == pygame.K_LEFT:
            self.move_handler.undo()
        elif event.key == pygame.K_RIGHT:
            self.move_handler.redo()
        else:
            pass

    def end_turn(self):
        """
        End turn, recalculate possible moves in the new position.
        """
        self.board.end_turn()
        self.board.deselect()
        self.clicks = []
        self.move_generator.generate_moves()

    def reset_clicks(self):
        """
        Reset GUI state of the board without triggering change of player.
        """
        self.board.deselect()
        self.clicks = []

    def hitSquare(self, pos: Tuple[int, int]) -> Optional[Square]:
        for square in self.board:
            if square.rect.collidepoint(pos):
                return square
