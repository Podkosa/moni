from abc import ABC, abstractmethod

import asyncio
from typing import Coroutine

from conf.settings import logger
from handlers.abstract import Handler


class CheckerError(Exception):
    pass


class Checker(ABC):
    """
    Base checker class. An instance represents a single server.
    Knows how to run, check and alert itself, start periodic monitoring.
    """
    def __init__(
        self, host: str,
        port: int | None = None,
        handlers: list[Handler] = [],
        cycle: int | float | None = None,
        include_normal: bool = False    # Alert regardless of status
        ):
        self.host = host
        self.port = port
        self.handlers = handlers
        self.cycle = cycle
        self.include_normal = include_normal

    def __str__(self):
        return f'{self.__class__.__name__}({self.host})'

    async def run(self):
        """Run a check, store results, alert if something is not normal."""
        self.result = await self.check()
        if not self.result['status'] or self.include_normal:
            await self.alert(self.result['message'])

    async def alert(self, message: str):
        """Send message through handlers"""
        async with asyncio.TaskGroup() as tg:
            for handler in self.handlers:
                tg.create_task(handler.handle(message))

    @abstractmethod
    async def check(self) -> dict:
        ...
        return {
            'host': str,
            'status': bool,
            'message': str
        }

    async def monitor(self) -> Coroutine:
        if not self.handlers or not self.cycle:
            raise CheckerError(f'Trying to start {self} monitoring without handlers or cycle defined.')
        while True:
            logger.info(f'Running {self}')
            try:
                await self.run()
            except:
                logger.exception(f'Exception during the monitoring {self}')
            else:
                logger.info(f'Finished {self}')
            await asyncio.sleep(self.cycle)  # type: ignore
