#!/usr/bin/env python3

import asyncio

import settings, checkers
from settings import logger


async def watch():
    """Watchdog entrypoint"""
    logger.info('Watchdog is running.')
    while True:
        logger.info('Watchdog: checking servers')
        try:
            await checkers.check_all()
        except:
            logger.exception('Watchdog: Exception during the monitoring.')
        else:
            logger.info('Watchdog: all checks are finished')
        await asyncio.sleep(settings.WATCHDOG['cycle'])

if __name__ == '__main__':
    asyncio.run(watch())
