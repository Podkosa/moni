from conf import settings

import handlers


def get_handler_cls(handler_name: str):
    if handler_name not in settings.HANDLERS:
        raise ValueError(f'Handler {handler_name} is not defined in settings')
    return getattr(handlers, f'{handler_name.capitalize()}Handler')
