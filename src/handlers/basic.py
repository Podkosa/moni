import pathlib

import aiofiles, aiohttp

from conf import settings
from conf.settings import logger
from util.messages import timestamp, flatten
from util import aio_requests
from .abstract import Handler


class ConsoleHandler(Handler):
    async def _send_message(self, result: dict):
        final_message = f"{timestamp()} {flatten(result['message'])}"
        logger.info(final_message)

class LogHandler(Handler):
    def __init__(self):
        self.dir: pathlib.Path = settings.WORK_DIR / 'logs'
        self.dir.mkdir(exist_ok=True)
        self.path: pathlib.Path = self.dir  / settings.HANDLERS['log']['filename']

    async def _send_message(self, result: dict):
        final_message = f"{timestamp()} {flatten(result['message'])}\n"
        async with aiofiles.open(self.path, mode='a') as f:
            await f.write(final_message)

class WebhookHandler(Handler):
    def __init__(self):
        conf: dict = settings.HANDLERS['webhook']
        self.url: str = conf['url']
        self.user: str | None = conf.get('user')
        self.password: str | None = conf.get('password')
        self.headers: dict | None = conf.get('headers')
        self.cookies: dict | None = conf.get('cookies')

    async def _send_message(self, result: dict):
        auth = None
        if self.user and self.password:
            auth = aiohttp.BasicAuth(self.user, self.password)
        await aio_requests.post(
            self.url,
            data=result,
            auth=auth,
            headers=self.headers,
            cookies=self.cookies,
            response_type='ignore'
        )
