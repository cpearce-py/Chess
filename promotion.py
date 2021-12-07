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
    automatically align them horizontally, draw them to a surface and deal
    with triggering their action if clicked.

    Not the max_objects keyword argument is used to pre-setup the width/height
    of the layout. By default this is 4. You cannot add more tiles than the
    max_objects is set too. No error is thrown class will just ignore additional
    attempts to add more.

    By default, the widget is created at position (0,0) of the screen.
    Pass keyword arugment `position` to change this behaviour, or use move() method
    passing a tuple (x, y).

    Usage:
        l = Layout(max_objects=5)

        for tile in tiles:
            l.add_tile(tile)

        for event in pygame.event.get():
            l.handle_event(event)

        l.update()
        l.draw(surface)

    Layout class cannot control it's visibilty so up to user to create and destroy
    within game loop.

    This class creates a horizontally layouted widget, use subclass `VLayout`
    to create a vertical layout that works in the same way.
    """

    def __init__(self, max_objects: int = 4, **kwargs):

        self.max_objects = max_objects

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
        """
        Move layout widget, and all it's containing tiles, by some coordinate.

        :param amount: (x, y) move to apply to layout.
        :amount type: `tuple`, `list`, or `int`. If Int, will apply the same value
                      to both X and Y.
        """
        if not isinstance(amount, (tuple, list)):
            amount = (amount, amount)

        self.popup_rect.move_ip(amount)
        for obj in self._tiles.sprites():
            obj.rect.move_ip(amount)

    def update(self):
        self._tiles.update()

    def handle_event(self, event):
        for obj in self._tiles.sprites():
            if obj.check_click(event.pos):
                obj.action(piece=obj.name)

    def add_tile(self, tile):
        if len(self._tiles.sprites()) >= 4:
            return
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

    def __init__(self, max_objects: int=4, **kwargs):
        height = c.SQ_SIZE * max_objects
        width = c.SQ_SIZE
        super().__init__(max_objects=max_objects, height=height, width=width, **kwargs)

    def add_tile(self, tile):
        self._tiles.add(tile)
        rect = self.popup_rect.move(self.position)
        number_of_tiles = len(self._tiles.sprites())
        left = rect.left
        top = rect.top + (c.SQ_SIZE * (number_of_tiles - 1))
        tile.rect.top = top
        tile.rect.left = left

def _dummy_action(piece=None):
    if piece:
        print(f'Clicked: {piece}')
        return
    print("No action assigned")


class Tile(pygame.sprite.Sprite):
    """
    Subclass of pygame.sprite.Sprite, designed to be a GUI utility where you can
    place an image onto a BG colour tile.
    Example is used in Pawn promotion to show which piece you can promote too.

    :param image: pygame.Surface with image.
    :param bg_color: List or Tuple with RGB colour values.
    :param highlighted: `List` or `tuple` with RGB colour values.
    :param action: callable action that will be triggered when tile is clicked.

    kwargs:
        :param name: Optional name for the tile. Aimed at debugging.

    """
    def __init__(self, image, bg_color, highlighted=None,
                 action=_dummy_action, **kwargs):

        self.name = kwargs.pop('name', "Piece")
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

    layout = Layout(position=(50,100))

    for name, piece in BLACK_PIECES.items():
        tile = Tile(piece, (125,50,50), highlighted=(111,80,125), name=name)
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
                layout.handle_event(event)

        layout.update()
        screen.fill(_BLACK)
        layout.draw(screen)

        pygame.display.flip()
        clock.tick(c.FPS)


if __name__ == '__main__':
    main()
