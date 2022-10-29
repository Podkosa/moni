import asyncio

from conf import settings
import checkers, handlers
from checkers.abstract import Checker


def get_checker_cls(checker_name: str) -> type[Checker]:
    if checker_name not in settings.CHECKERS:
        raise ValueError(f'Checker {checker_name} is not defined in settings')
    return getattr(checkers, f'{checker_name.capitalize()}Checker')

def get_loaded_checkers() -> tuple[Checker]:
    """Loads, caches and returns checker instances."""
    if not checkers.__loaded_checkers__:
        for checker_name, conf in settings.CHECKERS.items():
            Checker_cls = get_checker_cls(checker_name)
            for server, params in conf['servers'].items():
                handler_names = params.pop('handlers')
                if not handler_names:
                    raise settings.SettingsError(f'No handlers defined for {checker_name} checker')
                params['handlers'] = [handlers.get_handler_cls(handler_name)() for handler_name in handler_names]
                checker = Checker_cls(host=server, **params)
                checkers.__loaded_checkers__.append(checker)
    return tuple(checkers.__loaded_checkers__)

async def full_check():
    """Run all checks from settings.CHECKERS. Alert through handlers."""
    await asyncio.gather(*(checker.run() for checker in get_loaded_checkers()))

async def monitor():
    """Start full monitoring"""
    await asyncio.gather(*(checker.monitor() for checker in get_loaded_checkers()))
    # As of 29.10.2022 `async with asyncio.TaskGroup` doesn't seem to be working when Watchdog is started as a script.
    # Never get's to execute anything from the `async with` body. Possible Python 3.11 bug, further investigation required.
