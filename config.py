import json
import string

RESOLUTION_WIDTH = "resolution-width"
RESOLUTION_HEIGHT = "resolution-height"
STARTING_SCENE = "starting-scene"
DEBUG = "debug"

cfg = None


def load_config():
    global cfg
    config_json_file = open('config.json')
    try:
        lines = [line.rstrip() for line in config_json_file]
        config_json = " ".join(lines)
        cfg = json.loads(config_json)
    finally:
        config_json_file.close()


def get(key):
    return cfg.get(key)

def get_resolution():
    width = get(RESOLUTION_WIDTH) or 1024
    height = get(RESOLUTION_HEIGHT) or 768
    return (width, height)

def get_scale():
    res = get_resolution()
    if res == (1024, 768):
        return 1
    elif res == (800, 600):
        return 0.78125

def is_debug():
    val = get(DEBUG)
    return val and val == True
