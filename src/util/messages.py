import traceback

def prepare_error_message(e: Exception) -> str:
    return ''.join(traceback.format_exception(e))
