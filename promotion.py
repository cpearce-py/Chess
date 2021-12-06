import os
from collections import deque

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

    _MAX_SPACES = 4

    def __init__(self, max_objects=None, *objects ):
        if not max_objects:
            max_objects = Layout._MAX_SPACES
        self._objects = deque(objects, maxlen=max_objects)
        self._tiles = pygame.sprite.Group(*objects)
        self._rect = None
        self._displayed = False

    def __len__(self):
        return len(self._tiles.sprites())

    def __repr__(self):
        return f"<{self.__class__.__name__} {repr(self._objects)}>"

    def show(self):
        """Display the layout"""
        self._displayed = True
        while self._displayed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    for tile in self._tiles:
                        tile.handle_event(event)
                        self._displayed = False

    @property
    def rect(self):
        if not self._tiles.sprites():
            # return pygame.Rect()
            pass

        length = len(self._tiles.sprites())
        width = c.SQ_SIZE*length
        height = c.SQ_SIZE
        self._rect
        return

    def update(self, *args):
        for object in self._objects:
            object.update(*args)

    def handle_event(self, event):
        if event == pygame.event.MOUSEBUTTONUP and event.key == 1:
            for obj in self._objects:
                if obj.check_clicked(event.pos):
                    return obj.action

    def add_tile(self, tile):
        self._tiles.add(tile)


    def _add_internal(self, *objects):
        self._objects.extend(objects)

    def draw(self, surface):
        return

class VLayout(Layout):
    def __init__(self, width=c.SQ_SIZE, height=None, maxlen=4):
        self.width = width
        self.height = c.SQ_SIZE * maxlen if not height else height

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

    HEIGHT = int(len(WHITE_PIECES)*c.SQ_SIZE)

    layout = Layout()

    for piece in BLACK_PIECES.values():
        tile = Tile(piece, (125,50,50), highlighted=(111,80,125))
        layout.add_tile(tile)

    # piece = WHITE_PIECES['wN']
    # t1 = Tile(piece, (125,50,50), highlighted=(111,80,125))


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
        # layout.update(pygame.mouse.get_pos())
        screen.fill(_BLACK)
        # layout.draw(screen)
        layout.draw(screen)


        pygame.display.flip()
        clock.tick(c.FPS)


if __name__ == '__main__':
    main()
