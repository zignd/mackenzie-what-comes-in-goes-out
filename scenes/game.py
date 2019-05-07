import pygame
import assets.images as images
from helpers import scale_pair, load_image
from scenes.names import GAME_SCENE
from .gamemap import MAP


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
        self.base.blit(self.background, scale_pair((0, 0)))
        self.base.blit(self.icon, scale_pair((7, 52)))
        self.base.blit(self.vessel, scale_pair((68, 17)))
        self.base.blit(self.get_filling(), scale_pair((76, 26)))
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


def resolve_next_code(c, c1, c2, c3):
    if c in (c1, c2, c3):
        if c == c1:
            return c2
        elif c == c2:
            return c3
        else:
            return c1
    else:
        return c1


class GameScene:
    def __init__(self, win):
        self.win = win

        self.satiety_gauge = Gauge(self.win, Gauge.TYPE_HIGH_IS_GOOD, load_image(
            images.PLATE_EMOJI), scale_pair((144, 595)))

        self.hygiene_gauge = Gauge(self.win, Gauge.TYPE_HIGH_IS_GOOD, load_image(
            images.SHOWER_EMOJI), scale_pair((439, 595)))

        self.toilet_gauge = Gauge(self.win, Gauge.TYPE_LOW_IS_GOOD, load_image(
            images.TOILET_EMOJI), scale_pair((748, 595)))

        self.components = [self.satiety_gauge,
                           self.hygiene_gauge, self.toilet_gauge]

        self.background = load_image(images.BRICK_WALL_BACKGROUND)
        self.marble = load_image(images.MARBLE)
        self.game_canvas = load_image(images.GAME_CANVAS)

        self.map_tiles = {
            'floor': load_image(images.TILE_FLOOR),
            'wall': load_image(images.TILE_WALL),
            'char11': load_image(images.TILE_CHAR11),
            'char12': load_image(images.TILE_CHAR12),
            'char13': load_image(images.TILE_CHAR13),
            'char21': load_image(images.TILE_CHAR21),
            'char22': load_image(images.TILE_CHAR22),
            'char23': load_image(images.TILE_CHAR23),
            'char31': load_image(images.TILE_CHAR31),
            'char32': load_image(images.TILE_CHAR32),
            'char33': load_image(images.TILE_CHAR33),
            'char41': load_image(images.TILE_CHAR41),
            'char42': load_image(images.TILE_CHAR42),
            'char43': load_image(images.TILE_CHAR43),
        }
        self.map_layers = {
            1: {'type': 'normal', 'tile': 'floor'},
            2: {'type': 'block', 'tile': 'wall'},
            11: {'type': 'char', 'tile': 'char11'},
            12: {'type': 'char', 'tile': 'char12'},
            13: {'type': 'char', 'tile': 'char13'},
            21: {'type': 'char', 'tile': 'char21'},
            22: {'type': 'char', 'tile': 'char22'},
            23: {'type': 'char', 'tile': 'char23'},
            31: {'type': 'char', 'tile': 'char31'},
            32: {'type': 'char', 'tile': 'char32'},
            33: {'type': 'char', 'tile': 'char33'},
            41: {'type': 'char', 'tile': 'char41'},
            42: {'type': 'char', 'tile': 'char42'},
            43: {'type': 'char', 'tile': 'char43'},
        }
        self.map_cells = MAP
        self.current_player_pos = (6, 7)

        self.map = pygame.Surface(self.game_canvas.get_size())

    def draw_map(self):
        self.map.blit(self.game_canvas, scale_pair((0, 0)))
        for i, line in enumerate(self.map_cells):
            for j, cell in enumerate(line):
                pos = scale_pair((j * 48, i * 48))
                for code in cell:
                    layer = self.map_layers[code]
                    self.map.blit(self.map_tiles[layer['tile']], pos)

    def move_player(self, direction):
        row, column = self.current_player_pos
        code = self.map_cells[row][column].pop()
        if direction == 'up':
            if row > 0:
                row -= 1
            code = resolve_next_code(code, 41, 42, 43)
        elif direction == 'right':
            if column < len(self.map_cells[0]) - 1:
                column += 1
            code = resolve_next_code(code, 31, 32, 33)
        elif direction == 'left':
            if column > 0:
                column -= 1
            code = resolve_next_code(code, 21, 22, 23)
        elif direction == 'down':
            if row < len(self.map_cells) - 1:
                row += 1
            code = resolve_next_code(code, 11, 12, 13)
        self.current_player_pos = (row, column)
        self.map_cells[row][column].append(code)

    # def can_player_move(self, direction):
    #     row, column = self.current_player_pos
    #     if row == 0 or row == (len(self.map_cells) - 1)
    #     or column == 0 or column == (len(self.map_cells[0]) - 1):
    #         return False
    #     if direction == 'up':
    #         row -= 1
    #     elif direction == 'right':
    #         column += 1
    #     elif direction == 'down':
    #         row += 1
    #     elif direction == 'left':
    #         column -= 1
    #     cell = self.map_cells[row][column]
    #     for code in cell:
    #         # TODO: return False if any of the codes points to a layer whose type is 'block'
    #         pass
    #     return True

    def render(self, **args):
        for event in args['events']:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move_player('up')
                    self.satiety_gauge.increase()
                elif event.key == pygame.K_RIGHT:
                    self.move_player('right')
                    self.toilet_gauge.increase()
                elif event.key == pygame.K_DOWN:
                    self.move_player('down')
                    self.satiety_gauge.decrease()
                elif event.key == pygame.K_LEFT:
                    self.move_player('left')
                    self.toilet_gauge.decrease()

        self.win.blit(self.background, scale_pair((0, 0)))
        self.win.blit(self.marble, scale_pair((110, 24)))
        self.win.blit(self.map, scale_pair((129, 40)))

        for component in self.components:
            component.draw()

        self.draw_map()

        return {'goto': GAME_SCENE}
