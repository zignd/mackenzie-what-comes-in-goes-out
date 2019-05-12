import pygame
import assets.images as images
from helpers import scale_pair, load_image
from scenes.names import START_SCENE, HOW_TO_PLAY_SCENE

class HowToPlayScene:
    def __init__(self, win):
        self.win = win

    def render(self, **args):
        return {'goto': HOW_TO_PLAY_SCENE}
        
        background = load_image(images.BACKGROUND)
        self.win.blit(background, (0, 0))
