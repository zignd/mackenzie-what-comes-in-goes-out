import os


def _path(name):
    return os.path.abspath(os.path.join('assets', 'images', name))


BACKGROUND = _path('background.png')
SELECTION_ARROW = _path('selection_arrow.png')
START_GAME_BUTTON = _path('start_game_button.png')
HOW_TO_PLAY_BUTTON = _path('how_to_play_button.png')
CREDITS_BUTTON = _path('credits_button.png')

BRICK_WALL_BACKGROUND = _path('brick_wall_background.png')
GAUGE_BACKROUND = _path('gauge_background.png')
PLATE_EMOJI = _path('plate_emoji.png')
SHOWER_EMOJI = _path('shower_emoji.png')
TOILET_EMOJI = _path('toilet_emoji.png')
GAUGE_TYPE1_FILL1 = _path('gauge_type1_fill1.png')
GAUGE_TYPE1_FILL2 = _path('gauge_type1_fill2.png')
GAUGE_TYPE1_FILL3 = _path('gauge_type1_fill3.png')
GAUGE_TYPE1_FILL4 = _path('gauge_type1_fill4.png')
GAUGE_TYPE1_FILL5 = _path('gauge_type1_fill5.png')
GAUGE_TYPE2_FILL1 = _path('gauge_type2_fill1.png')
GAUGE_TYPE2_FILL2 = _path('gauge_type2_fill2.png')
GAUGE_TYPE2_FILL3 = _path('gauge_type2_fill3.png')
GAUGE_TYPE2_FILL4 = _path('gauge_type2_fill4.png')
GAUGE_TYPE2_FILL5 = _path('gauge_type2_fill5.png')
GAUGE_EMPTY = _path('gauge_empty.png')
GAUGE_VESSEL = _path('gauge_vessel.png')
GAME_CANVAS = _path('game_canvas.png')
MARBLE = _path('marble.png')