import pygame
import assets.images as images
from helpers import scale_pair, load_image
from scenes.names import GAME_SCENE
from .gamemap import MAP


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
            'bedsidetable': load_image(images.TILE_BEDSIDETABLE),
            'bed_part1': load_image(images.TILE_BED_PART1),
            'bed_part2': load_image(images.TILE_BED_PART2),
            'toilet_part1': load_image(images.TILE_TOILET_PART1),
            'toilet_part2': load_image(images.TILE_TOILET_PART2),
            'bathtub_part1': load_image(images.TILE_BATHTUB_PART1),
            'bathtub_part2': load_image(images.TILE_BATHTUB_PART2),
            'wardrobe_part1': load_image(images.TILE_WARDROBE_PART1),
            'wardrobe_part2': load_image(images.TILE_WARDROBE_PART2),
            'window': load_image(images.TILE_WINDOW),
            'small_table_flower': load_image(images.TILE_SMALL_TABLE_FLOWER),
            'bathroom_mirror': load_image(images.TILE_BATHROOM_MIRROR),
            'bathroom_sink': load_image(images.TILE_BATHROOM_SINK),
            'table_metal_vert': load_image(images.TILE_TABLE_METAL_VERT),
            'chair_left': load_image(images.TILE_CHAIR_LEFT),
            'couch_part1': load_image(images.TILE_COUCH_PART1),
            'couch_part2': load_image(images.TILE_COUCH_PART2),
            'table_glass_part1': load_image(images.TILE_TABLE_GLASS_PART1),
            'table_glass_part2': load_image(images.TILE_TABLE_GLASS_PART2),
            'television': load_image(images.TILE_TELEVISION),
            'couch_vert_part1': load_image(images.TILE_COUCH_VERT_PART1),
            'couch_vert_part2': load_image(images.TILE_COUCH_VERT_PART2),
            'padded_round_stool': load_image(images.TILE_PADDED_ROUND_STOOL),
            'shelf_books_part1': load_image(images.TILE_SHELF_BOOKS_PART1),
            'shelf_books_part2': load_image(images.TILE_SHELF_BOOKS_PART2),
            'shelf_books_part3': load_image(images.TILE_SHELF_BOOKS_PART3),
            'shelf_books_part4': load_image(images.TILE_SHELF_BOOKS_PART4),
            'telephone': load_image(images.TILE_TELEPHONE),
            'table': load_image(images.TILE_TABLE),
            'sculpture_bust': load_image(images.TILE_SCULPTURE_BUST),
            'painting_support': load_image(images.TILE_PAINTING_SUPPORT),
            'round_wood_stool': load_image(images.TILE_ROUND_WOOD_STOOL),
        }
        self.map_layers = {
            1: {'type': 'normal', 'tile': 'floor'},
            2: {'type': 'block', 'tile': 'wall'},
            3: {'type': 'block', 'tile': 'bedsidetable'},
            4: {'type': 'normal', 'tile': 'bed_part1'},
            5: {'type': 'normal', 'tile': 'bed_part2'},
            6: {'type': 'block', 'tile': 'toilet_part1'},
            7: {'type': 'toilet', 'tile': 'toilet_part2'},
            8: {'type': 'bathtub', 'tile': 'bathtub_part1'},
            9: {'type': 'bathtub', 'tile': 'bathtub_part2'},
            10: {'type': 'block', 'tile': 'window'},
            11: {'type': 'char', 'tile': 'char11'},
            12: {'type': 'char', 'tile': 'char12'},
            13: {'type': 'char', 'tile': 'char13'},
            14: {'type': 'block', 'tile': 'wardrobe_part1'},
            15: {'type': 'block', 'tile': 'wardrobe_part2'},
            16: {'type': 'block', 'tile': 'small_table_flower'},
            17: {'type': 'block', 'tile': 'bathroom_mirror'},
            18: {'type': 'block', 'tile': 'bathroom_sink'},
            19: {'type': 'block', 'tile': 'table_metal_vert'},
            20: {'type': 'normal', 'tile': 'chair_left'},
            21: {'type': 'char', 'tile': 'char21'},
            22: {'type': 'char', 'tile': 'char22'},
            23: {'type': 'char', 'tile': 'char23'},
            24: {'type': 'block', 'tile': 'couch_part1'},
            25: {'type': 'block', 'tile': 'couch_part2'},
            26: {'type': 'block', 'tile': 'table_glass_part1'},
            27: {'type': 'block', 'tile': 'table_glass_part2'},
            28: {'type': 'block', 'tile': 'television'},
            29: {'type': 'block', 'tile': 'couch_vert_part1'},
            30: {'type': 'block', 'tile': 'couch_vert_part2'},
            31: {'type': 'char', 'tile': 'char31'},
            32: {'type': 'char', 'tile': 'char32'},
            33: {'type': 'char', 'tile': 'char33'},
            34: {'type': 'block', 'tile': 'padded_round_stool'},
            35: {'type': 'block', 'tile': 'shelf_books_part1'},
            36: {'type': 'block', 'tile': 'shelf_books_part2'},
            37: {'type': 'block', 'tile': 'shelf_books_part3'},
            38: {'type': 'block', 'tile': 'shelf_books_part4'},
            39: {'type': 'block', 'tile': 'telephone'},
            40: {'type': 'block', 'tile': 'table'},
            41: {'type': 'char', 'tile': 'char41'},
            42: {'type': 'char', 'tile': 'char42'},
            43: {'type': 'char', 'tile': 'char43'},
            44: {'type': 'block', 'tile': 'sculpture_bust'},
            45: {'type': 'block', 'tile': 'painting_support'},
            46: {'type': 'normal', 'tile': 'round_wood_stool'},

        }
        self.map_cells = MAP
        self.current_player_pos = (6, 7)

        self.map = pygame.Surface(self.game_canvas.get_size())

        self.is_player_moving = False
        self.last_player_moving_direction = None

    def draw_map(self):
        self.map.blit(self.game_canvas, scale_pair((0, 0)))
        for i, line in enumerate(self.map_cells):
            for j, cell in enumerate(line):
                pos = scale_pair((j * 48, i * 48))
                for code in cell:
                    layer = self.map_layers[code]
                    self.map.blit(self.map_tiles[layer['tile']], pos)

    def move_player(self, direction):
        # in order to keep the player moving we need to keep track of
        # the last direction he chose. so that in the next call to render
        # even if there are no keydown events, we can still decide
        # on a direction for the user
        if direction == None:
            direction = self.last_player_moving_direction
        else:
            self.last_player_moving_direction = direction
        self.is_player_moving = True

        row, column = self.current_player_pos
        next_row, next_column = row, column
        
        code = self.map_cells[row][column].pop()
        next_code = code
        
        # calculates the next position and next tile, based
        # on the current position and the current tile
        if direction == 'up':
            if row > 0:
                next_row -= 1
            next_code = resolve_next_code(code, 41, 42, 43)
        elif direction == 'right':
            if column < len(self.map_cells[0]) - 1:
                next_column += 1
            next_code = resolve_next_code(code, 31, 32, 33)
        elif direction == 'left':
            if column > 0:
                next_column -= 1
            next_code = resolve_next_code(code, 21, 22, 23)
        elif direction == 'down':
            if row < len(self.map_cells) - 1:
                next_row += 1
            next_code = resolve_next_code(code, 11, 12, 13)
        
        # checks if the player will collide with a blocking tile by going to next position
        next_pos = (next_row, next_column)
        if self.can_player_move(next_pos):
            # moves the player to the next position, and updates the tile
            self.current_player_pos = next_pos
            self.map_cells[next_row][next_column].append(next_code)
        else:
            # keeps the player at the same position, updates only the tile
            self.map_cells[row][column].append(next_code)

    def stop_player(self):
        self.is_player_moving = False
        self.last_player_moving_direction = None

    def can_player_move(self, next_pos):
        next_row, next_column = next_pos
        next_cell = self.map_cells[next_row][next_column]
        for code in next_cell:
            if self.map_layers[code]['type'] == 'block':
                return False
        return True


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
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT):
                    self.stop_player()

        self.win.blit(self.background, scale_pair((0, 0)))
        self.win.blit(self.marble, scale_pair((110, 24)))
        self.win.blit(self.map, scale_pair((129, 40)))

        for component in self.components:
            component.draw()

        self.draw_map()

        return {'goto': GAME_SCENE}

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