from abc import ABC, abstractmethod

import pygame

from ui import Button
from Board import Board
from events.event_handler import GameHandler

BLUE = (106, 159, 181)
WHITE = (255,255, 255)
BLACK = (0,0,0)


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
    """ Simple main menu scene. """
    def __init__(self):
        super().__init__()
        _play_btn = Button(
            center_position=(200, 200),
            font_size=30,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Play Game",
            action=GameScene
        )

        _setting_btn = Button(
            center_position=(200, 100),
            font_size=20,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Setting",
            action=SettingScene
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
            action=Menu
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


class GameScene(Scene):
    """Main chess game scene."""
    def __init__(self):
        super().__init__()
        self.board = Board()
        self.game_handler = GameHandler(self.board, scene=self)

    def process_input(self, event):
        self.game_handler.handle_events(event)

    def update(self):
        self.board.update()

    def render(self, screen):
        screen.fill(BLACK)
        self.board.draw(screen)
        self.objects.draw(screen)
