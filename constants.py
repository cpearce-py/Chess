from enum import Enum
import pygame

WIDTH = HEIGHT = 512
DIMENSIONS = 8
SQ_SIZE = HEIGHT // DIMENSIONS
RANKS = [8, 7, 6, 5, 4, 3, 2, 1]

class Piece(Enum):
    King = 1
    Pawn = 2
    Knight = 3
    Bishop = 4
    Rook = 5
    Queen = 6

    White = 8
    Black = 16


class Files(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7
    H = 8


class Color(Enum):
    LIGHT = 1
    DARK = 2

def _setupImages(path):
    """
    Local method to load all our pieces images.
    """
    _IMAGES = {}
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ',
              'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        _IMAGES[piece] = pygame.transform.scale(
            pygame.image.load(f'{path}/{piece}.png'), (SQ_SIZE, SQ_SIZE))

    return _IMAGES
IMAGES = _setupImages('IMG')
