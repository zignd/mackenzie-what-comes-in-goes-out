import os
import sys
import pygame
import config
import assets


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


def main():
    pygame.init()

    resolution = config.get_resolution()
    win = pygame.display.set_mode(resolution)

    pygame.display.set_caption("What comes in, goes out!")

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        start_scene(win)
        pygame.display.update()


def start_scene(win):
    background = load_image(assets.BACKGROUND)
    win.blit(background, (0, 0))

    x = 328
    y = 341

    start_game_button = load_image(assets.START_GAME_BUTTON)
    win.blit(start_game_button, scale_pair((x, y)))

    space_between = 30
    height = start_game_button.get_height()

    how_to_play_button = load_image(assets.HOW_TO_PLAY_BUTTON)
    win.blit(how_to_play_button, scale_pair((x, y+height+space_between)))

    credits_button = load_image(assets.CREDITS_BUTTON)
    win.blit(credits_button, scale_pair((x, y+(height+space_between)*2)))

    start_cursor = load_image(assets.START_CURSOR)
    win.blit(start_cursor, scale_pair((204, 348)))


if __name__ == "__main__":
    config.load_config()
    main()
