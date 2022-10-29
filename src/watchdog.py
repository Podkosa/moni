#!/usr/bin/env python3

import asyncio
import uvloop

from conf.settings import logger
import checkers


class WatchdogError(Exception):
    pass


async def watch():
    """Watchdog entrypoint"""
    logger.info('Watchdog is running')
    await checkers.monitor()
    raise WatchdogError('Watchdog ended unexpectedly')


if __name__ == '__main__':
    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
        runner.run(watch())
