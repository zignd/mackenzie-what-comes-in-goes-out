from scenes.names import HOW_TO_PLAY_SCENE


class HowToPlayScene:
    def __init__(self, win):
        self.win = win

    def render(self, **args):
        return {'goto': HOW_TO_PLAY_SCENE}
