import pathlib
from datetime import datetime

import aiofiles

from conf import settings
from conf.settings import logger
from util.messages import timestamp, flatten
from .abstract import Handler


class LogHandler(Handler):
    async def _send_message(self, message: str):
        final_message = f"{timestamp()} {flatten(message)}"
        logger.info(final_message)

class FileHandler(Handler):
    def __init__(self):
        self.dir: pathlib.Path = settings.WORK_DIR / 'logs'
        self.dir.mkdir(exist_ok=True)
        self.path: pathlib.Path = self.dir  / settings.HANDLERS['file']['filename']

    async def _send_message(self, message: str):
        final_message = f"{timestamp()} {flatten(message)}\n"
        async with aiofiles.open(self.path, mode='a') as f:
            await f.write(final_message)
