import traceback
from datetime import datetime

from conf import settings


def prepare_error_message(checker, e: Exception, with_traceback: bool = False) -> str:
    if with_traceback:
        return ''.join(traceback.format_exception(e))
    else:
        if str(e):
            return f'{checker} {str(e)}'
        else:
            return f'{checker} {e.__class__.__name__}'


def timestamp() -> str:
    return datetime.now().strftime(settings.DTTM_FORMAT)

def flatten(string: str) -> str:
    return string.replace('\n', ' ')
