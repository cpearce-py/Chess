import pygame
import pygame.freetype
from pygame.sprite import Sprite

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
        self.mouse_over = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
