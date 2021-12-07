import os
from collections import deque
from typing import Tuple

import pygame

import constants as c

_BLACK = (0,0,0)


def _setup_images(path, pieces=None):

    IMAGES = {}

    if not pieces:
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ',
                'bp', 'bR', 'bN', 'bB', 'bK', 'bQ',]

    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(
            pygame.image.load(f'{path}/{piece}.png'), (c.SQ_SIZE, c.SQ_SIZE))

    return IMAGES


class Layout:
    """
    Base class, aimed at acting like a widget. Holds Tile objects and will
    automatically align them horizontally, draw them to the a surface and deal
    with triggering their action once clicked.

    Usage:
        l = Layout()

        for tile in tiles:
            l.add_tile(tile)

        for event in pygame.event.get():
            l.handle_event(event)

        l.update()
        l.draw(surface)

    Layout class cannot control it's visibilty so up to user to create and destroy
    within game loop.

    Can pass certain keyword arguments to affect the style of the layout,
    however it's safer to use the pre-defined subclassed layouts.
    ie. HLayout, VLayout.
    """
    _MAX_SPACES = 4

    def __init__(self, max_objects: int=None, **kwargs):

        if not max_objects:
            max_objects = Layout._MAX_SPACES

        self._tiles = pygame.sprite.Group()

        width = kwargs.pop('width', c.SQ_SIZE * max_objects)
        height = kwargs.pop('height', c.SQ_SIZE)
        self.position = kwargs.pop('position', (0,0))

        popup_rect = pygame.Rect((0,0), (width, height))
        popup_rect.move_ip(self.position)

        self.popup_rect = popup_rect

    def __len__(self):
        return len(self._tiles.sprites())

    def __repr__(self):
        return f"<{self.__class__.__name__} {len(self)}>"

    @property
    def rect(self):
        return self.popup_rect

    def move(self, amount):
        if not isinstance(amount, tuple):
            amount = (amount, amount)

        self.popup_rect.move_ip(amount)
        for obj in self._tiles.sprites():
            obj.rect.move_ip(amount)

    def update(self):
        self._tiles.update()

    def handle_event(self, event):
        for obj in self._tiles.sprites():
            if obj.check_click(event.pos):
                obj.action()

    def add_tile(self, tile):
        self._tiles.add(tile)
        rect = self.popup_rect.move(self.position)
        number_of_tiles = len(self._tiles.sprites())
        top = rect.top
        left = rect.left + (c.SQ_SIZE * (number_of_tiles-1))
        tile.rect.top = top
        tile.rect.left = left

    def draw(self, surface):
        for obj in self._tiles.sprites():
            obj.draw(surface)

class VLayout(Layout):

    def __init__(self, **kwargs):
        height = c.SQ_SIZE * Layout._MAX_SPACES
        width = c.SQ_SIZE
        super().__init__(height=height, width=width, **kwargs)

    def add_tile(self, tile):
        self._tiles.add(tile)
        rect = self.popup_rect.move(self.position)
        number_of_tiles = len(self._tiles.sprites())
        left = rect.left
        top = rect.top + (c.SQ_SIZE * (number_of_tiles - 1))
        tile.rect.top = top
        tile.rect.left = left

def _dummy_action():
    print("No action assigned")


class Tile(pygame.sprite.Sprite):
    """
    Subclass of pygame.sprite.Sprite, designed to be a GUI utility where you can
    place an image onto a BG colour tile.
    Example is used in Pawn promotion to show which piece you can promote too.

    :param image: pygame.Surface with image.
    :param bg_color: List or Tuple with RGB colour values.
    """
    def __init__(self, image, bg_color, highlighted=None, action=_dummy_action):
        self._mouse_over = False
        self.action = action

        if not highlighted:
            highlighted = bg_color
        self._bg_colors = (bg_color, highlighted)

        try:
            self.image = image.convert_alpha()
        except pygame.error:
            self.image = image
        self.rect = self.image.get_rect()

        super().__init__()

    @property
    def bg(self):
        return self._bg_colors[1] if self._mouse_over else self._bg_colors[0]

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if self.rect.collidepoint(event.pos):
            self.action()

    def update(self):
        self._mouse_over = self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, surface):
        surface.fill(self.bg, rect=self.rect)
        surface.blit(self.image, self.rect)


def main():
    IMG_FOLDER = os.path.join(os.path.dirname(__file__), 'IMG')

    WHITE_PIECES = _setup_images(IMG_FOLDER, pieces=['wR', 'wN', 'wB', 'wQ',])
    BLACK_PIECES = _setup_images(IMG_FOLDER, pieces=['bR', 'bN', 'bB', 'bQ',])

    layout = VLayout(position=(50,100))

    for piece in BLACK_PIECES.values():
        tile = Tile(piece, (125,50,50), highlighted=(111,80,125))
        layout.add_tile(tile)



    pygame.init()
    screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONUP:
                print('sending to layout')
                layout.handle_event(event)

        layout.update()
        screen.fill(_BLACK)
        layout.draw(screen)

        pygame.display.flip()
        clock.tick(c.FPS)


if __name__ == '__main__':
    main()
