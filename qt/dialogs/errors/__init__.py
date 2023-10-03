from qt.dialogs.errors.parents import ErrorDialog
from qt.dialogs.errors.error import KeyFileError


class ErrorWindows:
    __dict__ = {'KeyFileNotFound': KeyFileError,
                "UncategorizedError": ErrorDialog}

    def __getitem__(self, item: str):
        return self.__dict__[item] if item in self.__dict__ else self.__dict__['UncategorizedError']
