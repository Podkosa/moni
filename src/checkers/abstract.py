from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from handlers.abstract import Handler

@dataclass
class Checker(ABC):
    username: str
    password: str
    host: str
    port: str | int | None = None
    handlers: list[Handler] = field(default_factory=lambda: [])

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
