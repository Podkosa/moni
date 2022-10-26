import settings, handlers


def get_handlers_cls(handler_name: str):
    return getattr(handlers, f'{handler_name.capitalize()}Handler')
