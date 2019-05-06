import pygame
import assets.images as images
from helpers import load_image
from scenes.names import GAME_SCENE


class Gauge:
    def __init__(self, win, type, icon, pos):
        self.type = type
        self.win = win
        self.pos = pos

        if type == Gauge.TYPE_HIGH_IS_GOOD:
            self.current_value = Gauge.MAX_VALUE
            self.fillings = [
                load_image(images.GAUGE_TYPE1_FILL1),
                load_image(images.GAUGE_TYPE1_FILL2),
                load_image(images.GAUGE_TYPE1_FILL3),
                load_image(images.GAUGE_TYPE1_FILL4),
                load_image(images.GAUGE_TYPE1_FILL5),
            ]
        elif type == Gauge.TYPE_LOW_IS_GOOD:
            self.current_value = Gauge.MIN_VALUE
            self.fillings = [
                load_image(images.GAUGE_TYPE2_FILL1),
                load_image(images.GAUGE_TYPE2_FILL2),
                load_image(images.GAUGE_TYPE2_FILL3),
                load_image(images.GAUGE_TYPE2_FILL4),
                load_image(images.GAUGE_TYPE2_FILL5),
            ]
        else:
            raise Exception("Invalid gauge type")

        self.background = load_image(images.GAUGE_BACKROUND)
        self.icon = icon
        self.vessel = load_image(images.GAUGE_VESSEL)
        self.empty = load_image(images.GAUGE_EMPTY)

        self.base = pygame.Surface(self.background.get_size())
        color_key = pygame.Color(255, 0, 255, 255)
        self.base.fill(color_key)
        self.base.set_colorkey(color_key)

    def draw(self):
        self.base.blit(self.background, (0, 0))
        self.base.blit(self.icon, (7, 52))
        self.base.blit(self.vessel, (68, 17))
        self.base.blit(self.get_filling(), (76, 26))
        self.win.blit(self.base, self.pos)

    def get_filling(self):
        if self.current_value == 0:
            return self.empty
        else:
            return self.fillings[int(self.current_value - 1)]

    def increase(self):
        if self.current_value < Gauge.MAX_VALUE:
            self.current_value += 0.5

    def decrease(self):
        if self.current_value > Gauge.MIN_VALUE:
            self.current_value -= 0.5


Gauge.MAX_VALUE = 5
Gauge.MIN_VALUE = 0
Gauge.TYPE_HIGH_IS_GOOD = 1
Gauge.TYPE_LOW_IS_GOOD = 2


class GameScene:
    def __init__(self, win):
        self.win = win

        self.satiety_gauge = Gauge(self.win, Gauge.TYPE_HIGH_IS_GOOD, load_image(
            images.PLATE_EMOJI), (144, 595))

        self.hygiene_gauge = Gauge(self.win, Gauge.TYPE_HIGH_IS_GOOD, load_image(
            images.SHOWER_EMOJI), (439, 595))

        self.toilet_gauge = Gauge(self.win, Gauge.TYPE_LOW_IS_GOOD, load_image(
            images.TOILET_EMOJI), (748, 595))

        self.components = [self.satiety_gauge,
                           self.hygiene_gauge, self.toilet_gauge]

        self.background = load_image(images.BRICK_WALL_BACKGROUND)
        self.marble = load_image(images.MARBLE)
        self.game_canvas = load_image(images.GAME_CANVAS)

        self.map_tiles = {
            'fl': load_image(images.TILE_FLOOR),
            'c11': load_image(images.TILE_CHAR11),
        }

        # 16x11
        self.map_format = [
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 1
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 2
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 3
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 4
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 5
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 6
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl','c11'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 7
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 8
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 9
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 10
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 11
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 12
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 13
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 14
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 15
            [['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl'], ['fl']], # 16
        ]

        self.map = pygame.Surface(self.game_canvas.get_size())
    
    def draw_map(self):
        self.map.blit(self.game_canvas, (0, 0))
        for i, line in enumerate(self.map_format):
            for j, cell in enumerate(line):
                for key in cell:
                    self.map.blit(self.map_tiles[key], (i * 48, j * 48))

    def render(self, **args):
        for event in args['events']:
            if event.type == pygame.KEYDOWN:
                # TODO: remove
                if event.key == pygame.K_UP:
                    self.satiety_gauge.increase()
                elif event.key == pygame.K_RIGHT:
                    self.toilet_gauge.increase()
                elif event.key == pygame.K_DOWN:
                    self.satiety_gauge.decrease()
                elif event.key == pygame.K_LEFT:
                    self.toilet_gauge.decrease()

        self.win.blit(self.background, (0, 0))
        self.win.blit(self.marble, (110, 24))
        self.win.blit(self.map, (129, 40))

        for component in self.components:
            component.draw()

        self.draw_map()

        return {'goto': GAME_SCENE}
