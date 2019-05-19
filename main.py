import sys
import pygame
import config
import assets.images as images
from helpers import load_image
from scenes.names import START_SCENE, GAME_SCENE, GAME_OVER_SCENE, HOW_TO_PLAY_SCENE, CREDITS_SCENE
from scenes.start import StartScene
from scenes.game import GameScene
from scenes.game_over import GameOverScene
from scenes.howtoplay import HowToPlayScene
from scenes.credits import CreditsScene


def main():
    # initializing pygame
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    # setting up the game window
    resolution = config.get_resolution()
    win = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Tudo que entra, também sai")
    pygame.display.set_icon(load_image(images.TOILET_ICON))
    clock = pygame.time.Clock()

    # scenes dictionary, to ease the access
    router = {
        START_SCENE: StartScene(win),
        GAME_SCENE: None,
        GAME_OVER_SCENE: GameOverScene(win),
        HOW_TO_PLAY_SCENE: HowToPlayScene(win),
        CREDITS_SCENE: CreditsScene(win)
    }

    # current scene being rendered
    current_scene = router[config.get(config.STARTING_SCENE) or START_SCENE]

    prev_command = None
    command = None

    while 1:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif config.is_debug() and event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

        prev_command = command

        # renders a scene and receives a command from it
        if prev_command is not None:
            command = current_scene.render(events=events, more_args=prev_command.get('more_args'))
        else:
            command = current_scene.render(events=events)

        # when the previous command is not the game scene, it means we're starting a new game scene
        starting_at_game_scene = prev_command is None and command['goto'] == GAME_SCENE
        moving_to_game_scene = prev_command is not None and prev_command['goto'] != GAME_SCENE and command['goto'] == GAME_SCENE
        if starting_at_game_scene or moving_to_game_scene:
            router[GAME_SCENE] = GameScene(win)

        # the command contains a goto action indicating the next scene to be rendered
        current_scene = router[command['goto']]

        pygame.display.update()
        clock.tick(40)


if __name__ == "__main__":
    config.load_config()
    main()
