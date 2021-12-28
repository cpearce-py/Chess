from abc import ABC, abstractmethod
from enum import Enum, auto

import pygame

from ui import Button
from board import Board
from events.event_handler import GameHandler
from promotion import Layout, Tile
import constants as c

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQ = (232, 235, 239)
DARK_SQ = (125, 135, 150)
LIGHT_HIGHLIGHT = (252, 115, 120)
DARK_HIGHLIGHT = (145, 62, 75)


def _setup_promotion_images():
    """
    Filter out 4 pieces we want to display in promotion menu and order by
    most valuable.
    """
    imgs = c.IMAGES

    piece_order = ["Q", "R", "B", "N"]

    dark_dict = {"b" + key: imgs["b" + key] for key in piece_order}
    light_dict = {"w" + key: imgs["w" + key] for key in piece_order}

    return {
        c.Color.LIGHT: list(light_dict.values()),
        c.Color.DARK: list(dark_dict.values()),
    }


_PIECES = _setup_promotion_images()


class Scene(ABC):
    """
    Abstract Scene class to be inhereted by sub-scene classes.
    Scene's hold all visible objects and tie together the GUI and logic.
    All sub-classed Scenes inherit the .objects attribute, which is a pygame
    `Group` class. This is setup to hold each scene's objects and allows the easy
    convience of draw() and update() that a `pygame.sprite.Group` class offers.
    """

    def __init__(self):
        self.next = self
        self.objects = pygame.sprite.Group()

    @abstractmethod
    def process_input(self, events, pressed_keys):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen):
        pass

    def switch_to_scene(self, scene):
        self.next = scene

    def terminate(self):
        self.switch_to_scene(None)


class Menu(Scene):
    """Simple main menu scene."""

    def __init__(self):
        super().__init__()
        _play_btn = Button(
            center_position=(200, 200),
            font_size=30,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Play Game",
            action=GameScene,
        )

        _setting_btn = Button(
            center_position=(200, 100),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Setting",
            action=SettingScene,
        )

        self.objects.add(_play_btn, _setting_btn)

    def process_input(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for obj in self.objects:
                if obj.check_click(event.pos):
                    self.switch_to_scene(obj.action())

    def update(self):
        self.objects.update(pygame.mouse.get_pos())

    def render(self, screen):
        screen.fill(BLACK)
        self.objects.draw(screen)


class SettingScene(Scene):
    """Simple settings scene. As of yet, it is just to demonstrate the scene
    switching."""

    def __init__(self):
        super().__init__()
        _return_btn = Button(
            center_position=(200, 100),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Return To Menu",
            action=Menu,
        )

        self.objects.add(_return_btn)

    def process_input(self, event):

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for obj in self.objects:
                if obj.check_click(event.pos):
                    action = obj.action()
                    self.switch_to_scene(action)

    def update(self):
        self.objects.update(pygame.mouse.get_pos())

    def render(self, screen):
        screen.fill(BLACK)
        self.objects.draw(screen)


class State(Enum):

    PLAYING = auto()
    PROMOTING = auto()


class GameScene(Scene):
    """Main chess game scene."""

    def __init__(self):
        super().__init__()
        self.board = Board()
        self.game_handler = GameHandler(self.board, scene=self)
        self.promotion_menu = None
        self.state = State.PLAYING

    def promote(self, colour):
        images = _PIECES.get(colour)
        layout = Layout()
        for index, image in enumerate(images):
            bg_color = DARK_SQ if index % 2 == 0 else LIGHT_SQ
            highlight_color = DARK_HIGHLIGHT if index % 2 == 0 else LIGHT_HIGHLIGHT
            tile = Tile(image, bg_color, highlight_color)
            layout.add_tile(tile)
        layout.move(pygame.mouse.get_pos())
        self.promotion_menu = layout
        self.state = State.PROMOTING

    def process_input(self, event):
        if self.state == State.PROMOTING:
            self.promotion_menu.handle_event(event)
        else:
            self.game_handler.handle_events(event)

    def update(self):
        try:
            self.promotion_menu.update()
        except AttributeError:
            pass
        self.objects.update()
        self.board.update()

    def render(self, screen):
        screen.fill(BLACK)
        self.board.draw(screen)
        self.objects.draw(screen)
        try:
            self.promotion_menu.draw(screen)
        except AttributeError:
            pass
