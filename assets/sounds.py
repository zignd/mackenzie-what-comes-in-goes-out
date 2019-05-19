import os


def _path(name):
    return os.path.abspath(os.path.join('assets', 'sounds', name))

EATING = _path('eating.ogg')
PEEING = _path('peeing.ogg')
POOPING = _path('pooping.ogg')
SHOWERING = _path('showering.ogg')
SINK = _path('sink.ogg')
STEP = _path('step.ogg')
WALLBUMP = _path('wallbump.ogg')