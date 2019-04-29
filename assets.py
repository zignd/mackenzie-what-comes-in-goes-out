import os

_base_path = os.path.split(os.path.abspath(__file__))[0]
_prefix = os.path.join(_base_path, 'assets')

def build_path(name):
    return os.path.join(_prefix, name)

BACKGROUND = build_path('background.png')
START_CURSOR = build_path('start_cursor.png')
START_GAME_BUTTON = build_path('start_game_button.png')
HOW_TO_PLAY_BUTTON = build_path('how_to_play_button.png')
CREDITS_BUTTON = build_path('credits_button.png')
