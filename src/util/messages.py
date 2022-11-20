import traceback
from datetime import datetime

from conf import settings


def prepare_error_message(checker, e: Exception, with_traceback: bool = False) -> str:
    if with_traceback:
        return ''.join(traceback.format_exception(e))
    else:
        if str(e):
            message = f'{checker} {str(e)}'
        else:
            message = f'{checker} {e.__class__.__name__}'
        if notes := getattr(e, '__notes__', None):
            message += '. ' + ', '.join(notes)
        return message


def timestamp() -> str:
    return datetime.now().strftime(settings.DTTM_FORMAT)

def flatten(string: str) -> str:
    return string.replace('\n', ' ')
