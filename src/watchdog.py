#!/usr/bin/env python3

import asyncio

import uvloop

from conf.settings import logger
from conf import settings
import checkers, handlers


class WatchdogError(Exception):
    pass


async def watch():
    """Watchdog entrypoint"""
    logger.info('Watchdog is running')
    await checkers.monitor()
    raise WatchdogError('Watchdog ended unexpectedly')

async def on_startup():
    for handler_name in settings.ON_STARTUP_HANDLERS:
        handler: handlers.Handler = handlers.get_handler_cls(handler_name)()
        await handler.handle({'message': f"Moni's Watchdog is up"})

async def on_shutdown():
    # Not implemented
    for handler_name in settings.ON_STARTUP_HANDLERS:
        handler: handlers.Handler = handlers.get_handler_cls(handler_name)()
        await handler.handle({'message': f"Moni's Watchdog is down"})


if __name__ == '__main__':
    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
        runner.run(on_startup())
        runner.run(watch())
