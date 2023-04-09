import os
from enum import Enum

import pygame

__all__ = (
    "ROOT_DIR",
    "WIDTH",
    "HEIGHT",
    "DIMENSIONS",
    "SQ_SIZE",
    "RANKS",
    "Files",
    "Color",
    "IMAGES",
)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print(ROOT_DIR)
WIDTH = HEIGHT = 512
FPS = 60
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


def _setup_images(path, pieces=None):
    """
    Local method to load all our pieces images.
    """
    images = {}

    if not pieces:
        pieces = [
            "wp",
            "wR",
            "wN",
            "wB",
            "wK",
            "wQ",
            "bp",
            "bR",
            "bN",
            "bB",
            "bK",
            "bQ",
        ]

    for piece in pieces:
        images[piece] = pygame.transform.scale(
            pygame.image.load(f"{path}/{piece}.png"), (SQ_SIZE, SQ_SIZE)
        )

    return images


IMAGES = _setup_images(ROOT_DIR + "/IMG")
