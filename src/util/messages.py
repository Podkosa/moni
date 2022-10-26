import traceback

def prepare_error_message(e: Exception, with_traceback: bool = False) -> str:
    if with_traceback:
        return ''.join(traceback.format_exception(e))
    else:
        return str(e)
