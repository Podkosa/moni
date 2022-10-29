from abc import ABC, abstractmethod

from conf.settings import logger


class HandlerError(Exception):
    pass


class Handler(ABC):
    """Base class for handlers."""
    def __str__(self):
        return f'{self.__class__.__name__}'

    async def handle(self, message: str):
        try:
            await self._send_message(message)
        except:
            logger.exception(f'Error sending message through {self}')

    @abstractmethod
    async def _send_message(self, message: str):
        ...
