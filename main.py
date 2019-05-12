import sys
import pygame
import config
from scenes.names import START_SCENE, GAME_SCENE, HOW_TO_PLAY_SCENE, CREDITS_SCENE
from scenes.start import StartScene
from scenes.game import GameScene
from scenes.howtoplay import HowToPlayScene
from scenes.credits import CreditsScene


def main():
    # initializing pygame
    pygame.init()
    pygame.mixer.init()  # TODO: will be used to play sounds

    # setting up the game window
    resolution = config.get_resolution()
    win = pygame.display.set_mode(resolution)
    pygame.display.set_caption("What comes in, goes out!")
    clock = pygame.time.Clock()

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
    current_scene = router[config.get(config.STARTING_SCENE) or START_SCENE]

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
        clock.tick(40)


if __name__ == "__main__":
    config.load_config()
    main()
