from conf.settings import logger
from .abstract import Handler


class LogHandler(Handler):
    async def handle(self, message: str):
        logger.info(message)
