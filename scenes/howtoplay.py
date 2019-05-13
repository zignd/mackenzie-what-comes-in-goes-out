import pygame
import assets.images as images
from helpers import scale_pair, load_image
from .names import START_SCENE, HOW_TO_PLAY_SCENE

class HowToPlayScene:
    def __init__(self, win):
        self.win = win
        self.button_init_pos_x = 328
        self.button_init_pos_y = 341
        self.button_height = 107
        self.button_space_between = 30

    def render(self, **args):
        return {'goto': HOW_TO_PLAY_SCENE}

        background = load_image(images.BACKGROUND)
        self.win.blit(background, (0, 0))

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return {'goto': START_SCENE}
