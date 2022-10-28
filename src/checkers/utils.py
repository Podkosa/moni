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
                handler_names = params.pop('handlers', [])
                params['handlers'] = [handlers.get_handler_cls(handler_name)() for handler_name in handler_names]
                checker = Checker_cls(host=server, **params)
                checkers.__loaded_checkers__.append(checker)
    return tuple(checkers.__loaded_checkers__)

async def check_all():
    """Run all checks from settings.CHECKERS. Alert through handlers."""
    async with asyncio.TaskGroup() as tg:
        for checker in get_loaded_checkers():
            tg.create_task(checker.run())

async def monitor():
    """Start full monitoring"""
    async with asyncio.TaskGroup() as tg:
        for checker in get_loaded_checkers():
            tg.create_task(checker.monitor())
