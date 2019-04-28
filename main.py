import os
import sys
import pygame
import config
import assets


def scale(surface):
    val = config.get_scale()
    width = int(surface.get_width() * val)
    height = int(surface.get_height() * val)
    return pygame.transform.scale(surface, (width, height))


def load_image(name):
    return pygame.image.load(name).convert()


def main():
    pygame.init()

    resolution = config.get_resolution()
    screen = pygame.display.set_mode(resolution)

    pygame.display.set_caption("What comes in, goes out!")

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        start_scene(screen)
        pygame.display.update()


def start_scene(screen):
    background = load_image(assets.BACKGROUND)
    background = scale(background)
    screen.blit(background, (0, 0))


if __name__ == "__main__":
    config.load_config()
    main()
