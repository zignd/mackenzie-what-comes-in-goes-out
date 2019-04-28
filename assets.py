import os

_base_path = os.path.split(os.path.abspath(__file__))[0]
_prefix = os.path.join(_base_path, 'assets')

BACKGROUND = os.path.join(_prefix, 'background.png')
