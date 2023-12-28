class GameCreationError(Exception):
    ...


class GameDeletionError(Exception):
    ...


class SubmitPlayError(Exception):
    ...


class InvalidMove(Exception):
    def __init__(self, message, *args):
        self.message = message
        super().__init__(*args)
