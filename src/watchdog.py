#!/usr/bin/env python3

import asyncio

from conf.settings import logger
import checkers


async def watch():
    """Watchdog entrypoint"""
    logger.info('Watchdog is running')
    await checkers.monitor()

if __name__ == '__main__':
    asyncio.run(watch())
