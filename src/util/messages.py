import traceback
from datetime import datetime

from conf import settings


def prepare_error_message(e: Exception, with_traceback: bool = False) -> str:
    if with_traceback:
        return ''.join(traceback.format_exception(e))
    else:
        return str(e)

def timestamp() -> str:
    return datetime.now().strftime(settings.DTTM_FORMAT)

def flatten(string: str) -> str:
    return string.replace('\n', ' ')
