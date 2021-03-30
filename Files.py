from enum import Enum
import pygame

WIDTH = HEIGHT = 512
DIMENSIONS = 8
SQ_SIZE = HEIGHT // DIMENSIONS

RANKS = [8, 7, 6, 5, 4, 3, 2, 1]


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


IMAGES = {}
pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ',
          'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
for piece in pieces:
    IMAGES[piece] = pygame.transform.scale(
        pygame.image.load(f'IMG/{piece}.png'), (SQ_SIZE, SQ_SIZE))
