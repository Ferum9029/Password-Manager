from storage.encryption.exceptions import KeyFileNotFound


class KeyDataDoesntFit(Exception):
    def __init__(self, *args):
        super().__init__(*args)
