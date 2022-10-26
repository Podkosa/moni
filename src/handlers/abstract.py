from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Handler(ABC):
    @abstractmethod
    async def handle(self, message: str):
        ...
