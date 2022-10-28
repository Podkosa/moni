from abc import ABC, abstractmethod
from handlers.abstract import Handler


class Checker(ABC):
    def __init__(self, host: str, port: int | None = None, handlers: list[Handler] = []):
        self.host = host
        self.port = port
        self.handlers = handlers

    async def run(self):
        self.result = await self.check()
        if not self.result['status']:
            await self.alert()
    
    async def alert(self):
        for handler in self.handlers:
            await handler.handle(self.result['message'])

    @abstractmethod
    async def check(self) -> dict:
        ...
        return {
            'host': str,
            'status': bool,
            'message': str
        }
