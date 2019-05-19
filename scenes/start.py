import pygame
import sys
import assets.images as images
from helpers import scale_pair, load_image
from .names import START_SCENE, GAME_SCENE, HOW_TO_PLAY_SCENE, CREDITS_SCENE

class StartScene:
    def __init__(self, win):
        self.win = win
        self.current_selection_index = 0
        self.button_init_pos_x = 328
        self.button_init_pos_y = 341
        self.button_height = 107
        self.button_space_between = 30

    def get_selection_arrow_position(self):
        x, y = 204, 348
        if self.current_selection_index == 0:
            return scale_pair((x, y))
        elif self.current_selection_index == 1:
            return scale_pair((x, y + self.button_height + self.button_space_between))
        else:
            return scale_pair((x, y + (self.button_height + self.button_space_between) * 2))

    def get_selected_scene(self):
        if self.current_selection_index == 0:
            return GAME_SCENE
        elif self.current_selection_index == 1:
            return HOW_TO_PLAY_SCENE
        elif self.current_selection_index == 2:
            return CREDITS_SCENE
        else:
            raise Exception(
                "Invalid selected scene index, can't map to a real scene")

    def render(self, **args):
        for event in args['events']:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_UP and self.current_selection_index > 0:
                    self.current_selection_index -= 1
                elif event.key == pygame.K_DOWN and self.current_selection_index < 2:
                    self.current_selection_index += 1
                elif event.key == pygame.K_RETURN:
                    return {'goto': self.get_selected_scene()}

        background = load_image(images.BACKGROUND)
        self.win.blit(background, (0, 0))

        start_game_button = load_image(images.START_GAME_BUTTON)
        self.win.blit(start_game_button, scale_pair(
            (self.button_init_pos_x, self.button_init_pos_y)))

        how_to_play_button = load_image(images.HOW_TO_PLAY_BUTTON)
        self.win.blit(how_to_play_button, scale_pair(
            (self.button_init_pos_x, self.button_init_pos_y + self.button_height + self.button_space_between)))

        credits_button = load_image(images.CREDITS_BUTTON)
        self.win.blit(credits_button, scale_pair(
            (self.button_init_pos_x, self.button_init_pos_y + (self.button_height + self.button_space_between) * 2)))

        selection_arrow = load_image(images.SELECTION_ARROW)
        self.win.blit(selection_arrow, self.get_selection_arrow_position())

        return {'goto': START_SCENE}