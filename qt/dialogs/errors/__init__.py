from qt.dialogs.errors.parents import ErrorDialog
from qt.dialogs.errors.dialogs import KeyFileNotFoundDialog, KeyDoesntFitDialog
from qt.dialogs.errors.error_codes import ErrorCodes


class ErrorWindows:
    __dict__ = {'KeyFileNotFound': KeyFileNotFoundDialog,
                "UncategorizedError": ErrorDialog,
                "KeyDataDoesntFit": KeyDoesntFitDialog}

    def __getitem__(self, item: str):
        return self.__dict__[item] if item in self.__dict__ else self.__dict__['UncategorizedError']
