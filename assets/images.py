import os


def _path(name):
    return os.path.abspath(os.path.join('assets', 'images', name))


BACKGROUND = _path('background.png')
SELECTION_ARROW = _path('selection_arrow.png')
START_GAME_BUTTON = _path('start_game_button.png')
HOW_TO_PLAY_BUTTON = _path('how_to_play_button.png')
CREDITS_BUTTON = _path('credits_button.png')
