import sys
from enum import Enum
from functools import partial
from storage import delete_db, delete_k_data_file


# the functions a user chooses from when dealing with an error
class ErrorHandlers(Enum):
    DELETE_DATABASE = partial(delete_db)
    CLOSE_PROGRAM = sys.exit
    DELETE_KEY_FILE = partial(delete_k_data_file)
