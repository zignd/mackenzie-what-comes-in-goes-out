import pygame
import assets.images as images
from helpers import scale_pair, load_image
from .names import START_SCENE, CREDITS_SCENE


class CreditsScene:
    def __init__(self, win):
        self.win = win
        self.background = load_image(images.CREDITS)


    def render(self, **args):
        for event in args['events']:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return {'goto': START_SCENE}

        self.win.blit(self.background, scale_pair((0, 0)))

        return {'goto': CREDITS_SCENE}
