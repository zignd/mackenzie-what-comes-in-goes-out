import json
import string

RESOLUTION_WIDTH = "resolution-width"
RESOLUTION_HEIGHT = "resolution-height"

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
    return cfg[key]


def get_resolution():
    width = cfg[RESOLUTION_WIDTH]
    height = cfg[RESOLUTION_HEIGHT]
    return (width, height)

def get_scale():
    res = get_resolution()
    if res == (1024, 768):
        return 1
    elif res == (800, 600):
        return 0.78125
