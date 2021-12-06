import sys

import pygame

import move_generator as mg
from fen import START_FEN, PositionInfo, load_from_fen
from move import Flag, Move, MoveHandler

_load_position = load_from_fen(START_FEN)

class GameHandler:

    def __init__(self, board, scene, load_position: PositionInfo=_load_position):
        self.clicks =  []
        self.board = board
        self.board.init(load_position)
        whiteToMove = load_position.whiteToMove
        self.move_handler = MoveHandler(board, whiteToMove=whiteToMove)
        self.move_handler.generate_moves()
        self.move_generator = mg.MoveGenerator(board)
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
                user_move = Move(fromSq, toSq)
                # move = self.move_generator.get_move(user_move)
                # if move:
                #     self.move_handler.make_move(move)
                #     if move.flag == Flag.PROMOTE:
                #         colour_to_promote = user_move.fromSq.piece.color
                #         self._scene.promote(colour_to_promote)
                #     self.end_turn()
                # else:
                #     self.reset_clicks()
                if self.move_handler.try_move(user_move):
                    self.end_turn()
                else:
                    self.reset_clicks()

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
        self.board.end_turn()
        self.clicks = []
        self.move_generator.generate_moves()

    def reset_clicks(self):
        self.board.deselect()
        self.clicks = []

    def hitSquare(self, pos):
        for square in self.board:
            if square.rect.collidepoint(pos):
                return square
