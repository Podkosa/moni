import handlers


class CheckerError(Exception):
    pass


def get_handler_cls(handler_name: str):
    return getattr(handlers, f'{handler_name.capitalize()}Handler')
