# Scene's available
from abc import ABC, abstractmethod

import pygame

from ui import Button
from ui.gamestates import GameState
from Board import Board
from events.event_handler import GameHandler


BLUE = (106, 159, 181)
WHITE = (255,255, 255)
BLACK = (0,0,0)


class Scene(ABC):
    """
    Abstract Scene class to be inhereted by sub-scene classes.
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

    def __init__(self):
        super().__init__()
        self.board = Board()
        self.event_handler = GameHandler(self.board)

    def process_input(self, event):
        self.event_handler.handle_events(event)

    def update(self):
        self.board.update()

    def render(self, screen):
        screen.fill(BLACK)
        self.board.draw(screen)
