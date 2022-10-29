from abc import ABC, abstractmethod
from typing import Coroutine

import asyncio
from fastapi import HTTPException

from conf import settings
from conf.settings import logger
from handlers.abstract import Handler


class CheckerError(Exception):
    pass


class Checker(ABC):
    """
    Base class for checkers. An instance represents a single server.
    Knows how to run, check and alert itself, start periodic monitoring.
    """
    name = ''

    def __init__(
        self, host: str,
        port: int | None = None,
        handlers: list[Handler] = [],
        cycle: int | float | None = None,
        protocol: str = 'https',
        include_normal: bool = False    # Alert regardless of status
        ):
        self.host = host
        self.port = port
        self.handlers = handlers
        self.cycle = cycle
        self.protocol = protocol
        self.include_normal = include_normal

    def __str__(self):
        return f'{self.__class__.__name__}({self.host})'

    async def run(self):
        """Run a check, store results, alert if something is not normal."""
        self.result = await self.check()
        if self.include_normal or not self.result['status']:
            await self.alert(self.result['message'])

    async def alert(self, message: str):
        """Send message through handlers"""
        await asyncio.gather(*(handler.handle(message) for handler in self.handlers))

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
            logger.debug(f'Running {self}')
            try:
                await self.run()
            except:
                logger.exception(f'Exception during the monitoring {self}')
            else:
                logger.debug(f'Finished {self}')
            await asyncio.sleep(self.cycle)  # type: ignore

    @classmethod
    async def check_hosts(cls, hosts: list[str] | None = None) -> list[dict]:
        servers = settings.CHECKERS.get(cls.name, {}).get('servers')
        if not servers:
            raise HTTPException(500, f"{cls.name.capitalize()}Checker doesn't have any servers")

        if hosts:
            try:
                hosts_to_check = {host: servers.pop(host) for host in hosts}
            except KeyError as e:
                raise HTTPException(400, f'Unknown host {e.args[0]}')
        else:
            hosts_to_check = servers

        tasks = (cls(host=host, include_normal=True, **params).check() for host, params in hosts_to_check.items())
        return await asyncio.gather(*tasks)

    @property
    def url(self):
        return f'{self.protocol}://{self.host}{self.port if self.port else ""}/'

    @property
    def _message_header(self):
        return f'Host: {self.host}\n'
