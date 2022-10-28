from conf.settings import logger
from .abstract import Handler


class LogHandler(Handler):
    async def _send_message(self, message: str):
        logger.info(message)
