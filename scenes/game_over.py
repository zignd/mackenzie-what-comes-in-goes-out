import pygame
import assets.images as images
from helpers import scale_pair, load_image
from scenes.names import START_SCENE, GAME_SCENE, GAME_OVER_SCENE


class GameOverScene:
    def __init__(self, win):
        self.win = win
        self.background = load_image(images.ENDING)
        self.selection_border = load_image(images.SELECTION_BORDER)
        self.replayarrow = load_image(images.REPLAYARROW)
        self.checkmark = load_image(images.CHECKMARK)

        self.selected_button_index = 0

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
                        return {'goto': GAME_SCENE}
                    elif self.selected_button_index == 1:
                        return {'goto': START_SCENE}

        self.win.blit(self.background, scale_pair((0, 0)))

        font = pygame.font.SysFont('Comic Sans MS', 30)

        clock = args['more_args']['clock'] // 1000
        clock_str = "Tempo: {0}s".format(clock)
        clock_surf = font.render(clock_str, True, (0, 0, 0))

        food_eaten = args['more_args']['food_eaten']
        food_eaten_str = "Itens consumidos: {0}".format(food_eaten)
        food_eaten_surf = font.render(food_eaten_str, True, (0, 0, 0))

        self.win.blit(clock_surf, scale_pair((413, 612)))
        self.win.blit(food_eaten_surf, scale_pair((345, 652)))

        if self.selected_button_index == 0:
            self.win.blit(self.selection_border, scale_pair((25, 630)))
        else:
            self.win.blit(self.selection_border, scale_pair((845, 630)))
        self.win.blit(self.replayarrow, scale_pair((51, 642)))
        self.win.blit(self.checkmark, scale_pair((870, 642)))

        return {'goto': GAME_OVER_SCENE, 'more_args': args['more_args']}
