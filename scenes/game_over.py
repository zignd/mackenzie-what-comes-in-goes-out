import pygame
import assets.images as images
from helpers import scale_pair, load_image
from scenes.names import START_SCENE, GAME_OVER_SCENE


class GameOverScene:
    def __init__(self, win):
        self.win = win
        self.background = load_image(images.ENDING)

    def render(self, **args):
        for event in args['events']:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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

        return {'goto': GAME_OVER_SCENE, 'more_args': args['more_args']}
