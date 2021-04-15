import logic
import pygame
from Files import RANKS, Color, Files, WIDTH, HEIGHT, DIMENSIONS, SQ_SIZE
from Location import Location
from Pieces import *
from Squares import Square


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
        super().__init__(self)
        self._lightPieces = []
        self._darkPieces = []
        self.tempPieces = pygame.sprite.Group()
        self.boardPieces = pygame.sprite.Group()
        self.selectedPiece = pygame.sprite.GroupSingle()
        self.takenPieces = pygame.sprite.Group()
        _BOARD = []
        _pieces = self._initialize()
        _map = {}

        for x, file in enumerate(Files):
            _strip = []
            colour = Color.DARK if x % 2 == 0 else Color.LIGHT
            for y, rank in enumerate(RANKS):
                rect = pygame.Rect(x*SQ_SIZE, y*SQ_SIZE, SQ_SIZE, SQ_SIZE)

                pos = Location(file, rank)
                _square = Square(colour, pos, rect)
                _square.add(self.boardPieces)
                pos.square = _square

                if _pieces.get(pos):
                    piece = _pieces.get(pos)
                    _square.currentPiece = piece
                    piece.square = _square
                    piece.add(self.tempPieces)
                    if piece.color == Color.DARK:
                        self.darkPieces.append(piece)
                    else:
                        self.lightPieces.append(piece)
                self.add(_square)
                _strip.append(_square)
                _map[pos] = _square

                colour = Color.LIGHT if colour == Color.DARK else Color.DARK

            _BOARD.append(_strip)

        self._BOARD = _BOARD
        self._map = _map
        # self.add(self.boardPieces.sprites())

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def getFile(self, square, direction):
        curFile = Files(square.location.file.value)
        newFile = Files(curFile.value + direction)
        newLocation = Location(newFile, square.location.rank)
        print(f'this is the new location: {newLocation}')
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
        self.boardPieces.draw(surface)
        self.tempPieces.draw(surface)
        self.selectedPiece.draw(surface)
        # pieces = []
        # for sqr in self.sprites():
        #     sqr.update()
        #     piece = sqr.currentPiece
        #     surface.blit(sqr.image, sqr.rect)
        #     if piece:
        #         piece.update()
        #         pieces.append(piece)
        # for piece in pieces:
        #     surface.blit(piece.image, piece.rect)

    def update(self):
        self.tempPieces.update(self.selectedPiece, self.tempPieces)
        self.selectedPiece.update(self.selectedPiece, self.tempPieces)
        self.boardPieces.update()


    def rank(self, row):
        i = len(self._BOARD) - row
        return self._BOARD[i]

    def file(self, col):
        file = []
        for row in self._BOARD:
            file.append(row[col])
        return file

    def printBoard(self):
        for i in range(len(self._BOARD)):
            line = " "
            line += f'{len(self._BOARD) - i} '
            for j in range(len(self._BOARD[i])):
                if self._BOARD[i][j].isOccupied:
                    piece = self._BOARD[i][j].currentPiece
                    line += f'{piece.name[0]} '
                else:
                    # Empty Square
                    line += f'- '
            print(line)
        line = "   "
        for file in Files:
            line += f'{file.name} '
        print(line)

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

    @staticmethod
    def _initialize():
        """ Initialise board in standard chess configuration."""
        pieces = {}

        # Rooks
        pieces[Location(Files.A, 1)] = Rook(Color.LIGHT)
        pieces[Location(Files.H, 1)] = Rook(Color.LIGHT)
        pieces[Location(Files.A, 8)] = Rook(Color.DARK)
        pieces[Location(Files.H, 8)] = Rook(Color.DARK)

        # Knights
        pieces[Location(Files.B, 1)] = Knight(Color.LIGHT)
        pieces[Location(Files.G, 1)] = Knight(Color.LIGHT)
        pieces[Location(Files.B, 8)] = Knight(Color.DARK)
        pieces[Location(Files.G, 8)] = Knight(Color.DARK)

        # Bishops
        pieces[Location(Files.C, 1)] = Bishop(Color.LIGHT)
        pieces[Location(Files.F, 1)] = Bishop(Color.LIGHT)
        pieces[Location(Files.C, 8)] = Bishop(Color.DARK)
        pieces[Location(Files.F, 8)] = Bishop(Color.DARK)

        # Queens
        pieces[Location(Files.D, 1)] = Queen(Color.LIGHT)
        pieces[Location(Files.D, 8)] = Queen(Color.DARK)

        # Kings
        pieces[Location(Files.E, 1)] = King(Color.LIGHT)
        pieces[Location(Files.E, 8)] = King(Color.DARK)

        # Pawns
        for file in Files:
            pieces[Location(file, 2)] = Pawn(Color.LIGHT)
            pieces[Location(file, 7)] = Pawn(Color.DARK)

        return pieces
