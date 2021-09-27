import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.sprite import RenderUpdates

BLUE = (106, 159, 181)
WHITE = (255,255, 255)

def create_surface_with_text(text, font_size, text_rgb, bg_rgb,
                             bold=True):
    """Returns surface with text written on"""
    font = pygame.freetype.SysFont("Courier", font_size, bold=bold)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class Button(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb,
                text_rgb, action=None):
        self.mouse_over = False
        _default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        _hightlighted_image = create_surface_with_text(
            text=text, font_size=font_size*1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [_default_image, _hightlighted_image]
        self.rects = [
            _default_image.get_rect(center=center_position),
            _hightlighted_image.get_rect(center=center_position)
        ]
        self.action =  action
        super(Button, self).__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def title_screen(screen):
    start_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME
    )

    quit_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return To Main Menu",
        action=GameState.QUIT
    )

    buttons = RenderUpdates(start_btn, quit_btn)

    return game_loop(screen, buttons)

def game_loop(screen, buttons):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
        buttons.draw(screen)
        pygame.display.flip()


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            game_state = play_level(screen)

        if game_state == GameState.QUIT:
            print('quitting')
            pygame.quit()
            return

if __name__ == "__main__":
    main()
