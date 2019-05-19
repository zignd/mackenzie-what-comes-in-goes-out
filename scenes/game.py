import random
import pygame
from pygame import time
import assets.images as images
import assets.sounds as sounds
from helpers import scale_pair, load_image
from scenes.names import START_SCENE, GAME_SCENE, GAME_OVER_SCENE
from .gameassets import get_map, LAYERS, get_tiles


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

        self.map_tiles = get_tiles()
        self.map_layers = LAYERS
        self.map_matrix = get_map()
        self.current_player_pos = (6, 7)

        self.map_surface = pygame.Surface(self.game_canvas.get_size())

        self.is_player_moving = False
        self.last_player_moving_direction = None

        self.time_event_id = pygame.USEREVENT+1
        self.walk_event_id = pygame.USEREVENT+2
        time.set_timer(self.time_event_id, 3000)
        self.clock = time.Clock()

        self.count_eaten_food = 0
        self.spawned_food = []
        self.spawn_food()

    def draw_map(self):
        self.map_surface.blit(self.game_canvas, scale_pair((0, 0)))
        for i, line in enumerate(self.map_matrix):
            for j, cell in enumerate(line):
                pos = scale_pair((j * 48, i * 48))
                for code in cell:
                    layer = self.map_layers[code]
                    self.map_surface.blit(self.map_tiles[layer['tile']], pos)

    def move_player(self, direction=None):
        if direction == None:
            direction = self.last_player_moving_direction
        else:
            self.last_player_moving_direction = direction
        self.is_player_moving = True

        row, column = self.current_player_pos
        next_row, next_column = row, column

        code = self.map_matrix[row][column].pop()
        next_code = code

        # calculates the next position and next tile, based
        # on the current position and the current tile
        if direction == 'up':
            if row > 0:
                next_row -= 1
            next_code = resolve_next_code(code, 41, 42, 43)
            play(sounds.STEP)
        elif direction == 'right':
            if column < len(self.map_matrix[0]) - 1:
                next_column += 1
            next_code = resolve_next_code(code, 31, 32, 33)
            play(sounds.STEP)
        elif direction == 'left':
            if column > 0:
                next_column -= 1
            next_code = resolve_next_code(code, 21, 22, 23)
            play(sounds.STEP)
        elif direction == 'down':
            if row < len(self.map_matrix) - 1:
                next_row += 1
            next_code = resolve_next_code(code, 11, 12, 13)
            play(sounds.STEP)

        # checks if the player will collide with a blocking tile by going to next position
        next_pos = (next_row, next_column)
        if self.can_player_move(next_pos):
            # moves the player to the next position, and updates the tile
            self.current_player_pos = next_pos
            self.map_matrix[next_row][next_column].append(next_code)
        else:
            # keeps the player at the same position, updates only the tile
            self.map_matrix[row][column].append(next_code)

    def stop_player(self):
        self.is_player_moving = False
        self.last_player_moving_direction = None

    def can_player_move(self, next_pos):
        next_row, next_column = next_pos
        next_cell = self.map_matrix[next_row][next_column]
        for code in next_cell:
            if self.map_layers[code]['type'] == 'block':
                return False
        return True

    def handle_gauges(self):
        self.satiety_gauge.decrease()
        self.hygiene_gauge.decrease()
        self.toilet_gauge.increase()

    def is_game_over(self):
        if self.satiety_gauge.current_value == Gauge.MIN_VALUE or self.hygiene_gauge.current_value == Gauge.MIN_VALUE:
            return True
        elif self.toilet_gauge.current_value == Gauge.MAX_VALUE:
            return True
        else:
            return False

    def handle_food(self):
        line, column = self.current_player_pos
        cell = self.map_matrix[line][column]
        food_code = None
        for code in cell:
            if self.map_layers[code]['type'] == 'food':
                food_code = code
                break
        if food_code is None:
            return
        self.spawned_food.remove(self.current_player_pos)
        cell.remove(code)
        self.satiety_gauge.increase(2)
        self.toilet_gauge.increase(1)
        self.spawn_food(1)
        self.count_eaten_food += 1
        play(sounds.EATING)

    def handle_shower(self):
        line, column = self.current_player_pos
        cell = self.map_matrix[line][column]
        found_shower = False
        for code in cell:
            if self.map_layers[code]['type'] == 'bathtub':
                found_shower = True
                break
        if not found_shower:
            return
        self.hygiene_gauge.increase(Gauge.MAX_VALUE)
        play(sounds.SHOWERING)

    def handle_sink(self):
        line, column = self.current_player_pos
        cell = self.map_matrix[line][column]
        found_sink = False
        for code in cell:
            if self.map_layers[code]['type'] == 'sink':
                found_sink = True
                break
        if not found_sink:
            return
        self.hygiene_gauge.increase(2)
        play(sounds.SINK)

    def handle_toilet(self):
        line, column = self.current_player_pos
        cell = self.map_matrix[line][column]
        found_toilet = False
        for code in cell:
            if self.map_layers[code]['type'] == 'toilet':
                found_toilet = True
                break
        if not found_toilet:
            return
        self.toilet_gauge.decrease(Gauge.MAX_VALUE)
        self.hygiene_gauge.decrease()
        play([sounds.PEEING, sounds.POOPING][random.choice((0, 1))])

    def handle_interaction(self):
        self.handle_food()
        self.handle_toilet()
        self.handle_shower()
        self.handle_sink()

    def spawn_food(self, k=None):
        possible = []
        for i, line in enumerate(self.map_matrix):
            for j, cell in enumerate(line):
                ok = True
                for code in cell:
                    if self.map_layers[code]['type'] != 'normal':
                        ok = False
                if ok:
                    possible.append((i, j))
        len_possible = len(possible)
        if k is None:
            k = len_possible // 13
        indexes = random.sample(range(len_possible), k)
        for i in indexes:
            self.spawned_food.append(possible[i])
            line, column = possible[i]
            self.map_matrix[line][column].append(self.get_random_food())

    def get_random_food(self):
        return random.choice([71, 72, 73, 74, 75, 76, 77])

    def render(self, **args):
        for event in args['events']:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return {'goto': START_SCENE}
                elif event.key == pygame.K_UP:
                    time.set_timer(self.walk_event_id, 400)
                    self.move_player('up')
                elif event.key == pygame.K_RIGHT:
                    time.set_timer(self.walk_event_id, 400)
                    self.move_player('right')
                elif event.key == pygame.K_DOWN:
                    time.set_timer(self.walk_event_id, 400)
                    self.move_player('down')
                elif event.key == pygame.K_LEFT:
                    time.set_timer(self.walk_event_id, 400)
                    self.move_player('left')
                elif event.key == pygame.K_SPACE:
                    self.handle_interaction()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT):
                    self.stop_player()
            elif event.type == self.time_event_id:
                self.handle_gauges()
            elif event.type == self.walk_event_id:
                self.move_player()

        self.win.blit(self.background, scale_pair((0, 0)))
        self.win.blit(self.marble, scale_pair((110, 24)))
        self.win.blit(self.map_surface, scale_pair((129, 40)))

        for component in self.components:
            component.draw()

        self.draw_map()

        if self.is_game_over():
            return {
                'goto': GAME_OVER_SCENE,
                'more_args': {
                    'clock': self.clock.tick(),
                    'food_eaten': self.count_eaten_food
                }
            }

        return {'goto': GAME_SCENE, 'more_args': args['more_args']}


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
        if self.current_value == 0.0:
            return self.empty
        else:
            return self.fillings[int(self.current_value - 1)]

    def increase(self, value=0.5):
        if self.current_value < Gauge.MAX_VALUE:
            if self.current_value + value > Gauge.MAX_VALUE:
                self.current_value = Gauge.MAX_VALUE
            else:
                self.current_value += value

    def decrease(self, value=0.5):
        if self.current_value > Gauge.MIN_VALUE:
            if self.current_value - value < Gauge.MIN_VALUE:
                self.current_value = Gauge.MIN_VALUE
            else:
                self.current_value -= value


Gauge.MAX_VALUE = 5.0
Gauge.MIN_VALUE = 0.0
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


def play(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()
