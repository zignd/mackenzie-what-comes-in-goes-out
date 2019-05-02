import os
import sys
import pygame
import config
import assets.images as images


# helper functions


def scale_pair(pair):
    val = config.get_scale()
    width, height = pair
    return (int(width * val), int(height * val))


def scale_surface(surface):
    pair = (surface.get_width(), surface.get_height())
    pair = scale_pair(pair)
    return pygame.transform.scale(surface, pair)


loaded_images = {}


def load_image(name):
    global loaded_images
    if loaded_images.get(name) == None:
        loaded_images[name] = scale_surface(
            pygame.image.load(name).convert_alpha())
    return loaded_images[name]


def load_sound(file):
    file = os.path.join(main_dir, 'data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print('Warning, unable to load, %s' % file)


# scenes
START_SCENE = 'start_scene'
GAME_SCENE = 'game_scene'
HOW_TO_PLAY_SCENE = 'how_to_play_scene'
CREDITS_SCENE = 'credits_scene'


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


class GameScene:
    def __init__(self, win):
        self.win = win

    def render(self, **args):
        return {'goto': GAME_SCENE}


class HowToPlayScene:
    def __init__(self, win):
        self.win = win

    def render(self, **args):
        return {'goto': HOW_TO_PLAY_SCENE}


class CreditsScene:
    def __init__(self, win):
        self.win = win

    def render(self, **args):
        return {'goto': CREDITS_SCENE}


# game bootstrap


def main():
    # initializing pygame
    pygame.init()
    pygame.mixer.init()  # TODO: will be used to play sounds

    # setting up the game window
    resolution = config.get_resolution()
    win = pygame.display.set_mode(resolution)
    pygame.display.set_caption("What comes in, goes out!")

    # scenes instances
    start_scene = StartScene(win)
    game_scene = GameScene(win)
    how_to_play_scene = HowToPlayScene(win)
    credits_scene = CreditsScene(win)

    # scenes dictionary, to ease the access
    router = {
        START_SCENE: start_scene,
        GAME_SCENE: game_scene,
        HOW_TO_PLAY_SCENE: how_to_play_scene,
        CREDITS_SCENE: credits_scene
    }

    # current scene being rendered
    current_scene = start_scene

    while 1:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        # renders a scene and receives a command from it
        command = current_scene.render(events=events)
        # the command contains a goto action indicating the next scene to be rendered
        current_scene = router[command['goto']]

        pygame.display.update()


if __name__ == "__main__":
    config.load_config()
    main()
