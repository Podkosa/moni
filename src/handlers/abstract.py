from abc import ABC, abstractmethod


class HandlerError(Exception):
    pass


class Handler(ABC):
    @abstractmethod
    async def handle(self, message: str):
        ...
