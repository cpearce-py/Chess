import pygame

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

        self._render_pieces = pygame.sprite.LayeredUpdates()
        self._light_pieces = pygame.sprite.Group()
        self._dark_pieces = pygame.sprite.Group()
        self.board_squares = pygame.sprite.Group()
        self._map = {}
        self.all_pieces = {Color.DARK: self._dark_pieces, 
                        Color.LIGHT: self._light_pieces
                        }


    def init(self, load_position: PositionInfo=start_position):
        self.whiteToMove = load_position.whiteToMove
        self.color_to_move = Color.LIGHT if self.whiteToMove else Color.DARK

        pieces = load_position.squares
        map = {}

        for x, file in enumerate(Files):
            colour = Color.DARK if x % 2 == 0 else Color.LIGHT
            for y, rank in enumerate(RANKS):
                rect = pygame.Rect(x*SQ_SIZE, y*SQ_SIZE, SQ_SIZE, SQ_SIZE)

                pos = Location(file, rank)
                square = Square(colour, pos, rect)

                # Add square to the drawable pieces.
                self.board_squares.add(square)

                pos.square = square

                if (piece := pieces.get(pos)):

                    square.piece = piece
                    piece.square = square

                    self._render_pieces.add(piece, layer=piece.layer)

                    if piece.color == Color.DARK:
                        self._dark_pieces.add(piece)
                    else:
                        self._light_pieces.add(piece)

                self.add(square)
                map[pos] = square
                colour = Color.LIGHT if colour == Color.DARK else Color.DARK

        self._map = map
        return self

    def __repr__(self):
        attrs = (
            ('Light Pieces', len(self.light_pieces)),
            ('Dark Pieces', len(self.dark_pieces))
        )
        inners = ', '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {inners}>'

    def _get_piece(self, name, color):
        pieces = self.all_pieces.get(color)
        return list(filter(lambda x: x.name == name, pieces))

    def king(self, color):
        return self._get_piece("king", color)[0]
    
    def queen(self, color):
        return self._get_piece("queen", color)

    def bishops(self, color):
        return self._get_piece("bishop", color)

    def rooks(self, color):
        return self._get_piece("rook", color)

    def knights(self, color):
        return self._get_piece("knight", color)

    def pawns(self, color):
        return self._get_piece("pawn", color)

    def pieces(self, color):
        return self.all_pieces.get(color)
        
    def kill_piece(self, piece):
        piece.kill()

    def reset_squares(self):
        for square in self.board_squares:
            square.isAttacked = False

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
        self._render_pieces.draw(surface)

    def update(self):
        self._render_pieces.update()
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
    def light_pieces(self):
        return self._light_pieces

    @property
    def dark_pieces(self):
        return self._dark_pieces

    def deselect(self):
        for sqr in self.sprites():
            sqr.deselect()

    def set_piece(self, piece, square):
        square = self._map.get(square.location)
        square.piece = piece
        if piece:
            self.add_piece(piece)

    
    def add_piece(self, piece):
        if piece.color == Color.DARK:
            self.dark_pieces.add(piece)
        else:
            self.light_pieces.add(piece)
        self._render_pieces.add(piece, layer=0)

    def end_turn(self):
        self.deselect()
        self.reset_squares()
        self.color_to_move = Color.DARK if self.color_to_move == Color.LIGHT else Color.LIGHT

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

