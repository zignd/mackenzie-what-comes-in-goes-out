import os
import pygame
import config


def scale_pair(pair):
    val = config.get_scale()
    width, height = pair
    return (round(width * val), round(height * val))


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
