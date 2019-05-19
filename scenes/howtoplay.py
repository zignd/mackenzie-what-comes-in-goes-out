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
        self.selected_button_index = 0

        self.background = load_image(images.BACKGROUND_EMPTY)
        self.selection_border = load_image(images.SELECTION_BORDER)
        self.arrow_left = load_image(images.ARROW_LEFT)
        self.arrow_right = load_image(images.ARROW_RIGHT)

        self.images = [
            load_image(images.MOVEMENT_EXAMPLE),
            load_image(images.INTERACT_EXAMPLE),
            load_image(images.OBJECT_EXAMPLE),
            load_image(images.ESC_EXAMPLE),
        ]

        self.current_image_index = 0

    def render(self, **args):
        for event in args['events']:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return {'goto': START_SCENE}
                elif event.key == pygame.K_LEFT and self.selected_button_index > 0:
                    self.selected_button_index -= 1
                elif event.key == pygame.K_RIGHT and self.selected_button_index < 1:
                    self.selected_button_index += 1
                elif event.key == pygame.K_RETURN:
                    if self.selected_button_index == 0:
                        if self.current_image_index == 0:
                            return {'goto': START_SCENE}
                        else:
                            self.current_image_index -= 1
                    elif self.selected_button_index == 1:
                        if self.current_image_index == len(self.images) - 1:
                            return {'goto': START_SCENE}
                        else:
                            self.current_image_index += 1

        self.win.blit(self.background, scale_pair((0, 0)))
        self.win.blit(
            self.images[self.current_image_index], scale_pair((110, 30)))
        if self.selected_button_index == 0:
            self.win.blit(self.selection_border, scale_pair((40, 630)))
        else:
            self.win.blit(self.selection_border, scale_pair((819, 630)))
        self.win.blit(self.arrow_left, scale_pair((61, 642)))
        self.win.blit(self.arrow_right, scale_pair((860, 642)))

        return {'goto': HOW_TO_PLAY_SCENE}
