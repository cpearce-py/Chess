import pygame

import logic
from constants import RANKS, Color, Files, WIDTH, HEIGHT, DIMENSIONS, SQ_SIZE
from Location import Location
from Pieces import *
from Squares import Square

from ui.gamestates import GameState
from fen import PositionInfo, START_FEN, load_from_fen

start_position = load_from_fen(START_FEN)

class Board(pygame.sprite.Group):
    """
    Representation of Chess Board. Manage piece movement and board display.
    board.map attribute is a dictionary pairing each instance of Location, to
    an instance of a square. This allows us to quickly access information on a
    square by it's given location.

    board.map = {Location(FIlE=A, RANK=1): Square(LOCATION(FILE=A, RANK=1))}

    Example:
        board.map.get(Location(A,1)).currentPiece

    Returns:
        Rook(Color=LIGHT, Location(A,1))
    """

    def __init__(self):
        super(Board, self).__init__(self)
        self._lightPieces = pygame.sprite.Group()
        self._darkPieces = pygame.sprite.Group()
        self.tempPieces = pygame.sprite.Group()
        self.board_squares = pygame.sprite.Group()
        self.selectedPiece = pygame.sprite.GroupSingle()
        self.takenPieces = pygame.sprite.Group()
        self.state = GameState.GAME
        self._map = {}

    def init(self, load_position: PositionInfo=start_position):

        _pieces = load_position.squares
        _map = {}

        for x, file in enumerate(Files):
            colour = Color.DARK if x % 2 == 0 else Color.LIGHT
            for y, rank in enumerate(RANKS):
                rect = pygame.Rect(x*SQ_SIZE, y*SQ_SIZE, SQ_SIZE, SQ_SIZE)

                pos = Location(file, rank)
                square = Square(colour, pos, rect)

                # Add square to the drawable pieces.
                self.board_squares.add(square)

                pos.square = square

                if (piece := _pieces.get(pos)):

                    square.currentPiece = piece
                    piece.square = square

                    self.tempPieces.add(piece)

                    if piece.color == Color.DARK:
                        self._darkPieces.add(piece)
                    else:
                        self._lightPieces.add(piece)

                self.add(square)
                _map[pos] = square
                colour = Color.LIGHT if colour == Color.DARK else Color.DARK

        self._map = _map

    def __repr__(self):
        attrs = (
            ('Light Pieces', len(self.lightPieces)),
            ('Dark Pieces', len(self.darkPieces))
        )
        inners = ', '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {inners}>'

    def kill_piece(self, piece):
        # if piece.color == Color.LIGHT:
        #     self.lightPieces.remove(piece)
        # else:
        #     self.darkPieces.remove(piece)
        piece.kill()

    def reset_squares(self):
        for square in self.board_squares:
            square.isAttacked = False

    def get_pieces_coloured(self, color):
        if color == Color.LIGHT:
            return self.lightPieces
        elif color == Color.DARK:
            return self.darkPieces
        else:
            raise ValueError(f"{color} doesn't exist!")

    def get_piece_from_loc(self, loc):
        return self.map.get(loc).currentPiece

    def getFile(self, square, direction):
        curFile = Files(square.location.file.value)
        newFile = Files(curFile.value + direction)
        newLocation = Location(newFile, square.location.rank)
        return self.map.get(newLocation)

    def getFileUp(self, square):
        return self.getFile(square, 1)

    def getFileDown(self, square):
        return self.getFile(square, -1)

    def draw(self, surface):
        """
        Draw method inherited from pygame.sprite.Group.
        Updates each square and redraws to given surface.

        :param surface: Type `pygame.Surface` surface to draw to
        """
        self.board_squares.draw(surface)
        self.tempPieces.draw(surface)
        self.selectedPiece.draw(surface)

    def update(self):
        self.tempPieces.update(self.selectedPiece, self.tempPieces)
        self.selectedPiece.update(self.selectedPiece, self.tempPieces)
        self.board_squares.update()

    def rank(self, row):
        i = len(self._BOARD) - row
        return self._BOARD[i]

    def file(self, col):
        file = []
        for row in self._BOARD:
            file.append(row[col])
        return file

    @property
    def map(self):
        return self._map

    @property
    def board(self):
        return self._BOARD

    @property
    def lightPieces(self):
        return self._lightPieces

    @property
    def darkPieces(self):
        return self._darkPieces

    def deselect(self):
        for sqr in self.sprites():
            sqr.deselect()

    def load_from_fen(self, fen):
        pieces = {}
        pieceTypeFromSymbol = {
            'k': King,
            'p': Pawn,
            'n':  Knight,
            'b': Bishop,
            'r': Rook,
            'q': Queen
        }
        fenBoard = fen.split(' ')[0]
        file = 0
        rank = 7

        for symbol in fenBoard:
            if symbol == '/':
                file = 0
                rank -= 1
            else:
                if symbol.isnumeric():
                    file += int(symbol)
                else:
                    pieceColour = Color.LIGHT if symbol.isupper() else Color.DARK
                    pieceType = pieceTypeFromSymbol.get(symbol.lower())
                    loc = Location(Files(file+1), rank+1)
                    pieces[loc] = pieceType(pieceColour)
                    file += 1

        return pieces
