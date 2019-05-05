from scenes.names import CREDITS_SCENE


class CreditsScene:
    def __init__(self, win):
        self.win = win

    def render(self, **args):
        return {'goto': CREDITS_SCENE}
