from .abstract import Handler
from settings import logger

class SlackHandler(Handler):
    async def handle(self, message: str):
       logger.info(message)
