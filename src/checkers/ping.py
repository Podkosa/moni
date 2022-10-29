import aiohttp, asyncio

from conf import settings
from conf.settings import logger
from .abstract import Checker
from util import aio_requests, messages


class PingChecker(Checker):
    name = 'ping'

    def __init__(self, endpoint: str | None = None, *args, **kwargs):
        self.endpoint = endpoint
        super().__init__(*args, **kwargs)    

    async def check(self) -> dict:
        try:
            await self._get_data()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.warning(f"Couldn't Ping {self.host}: {e}")
            status = False
            message = messages.prepare_error_message(e)
        else:
            status = True
            message = self._prepare_message()

        self.result = {
            'host': self.host,
            'status': status,
            'message': message
        }
        return self.result

    async def _get_data(self):
        self.status_code = await aio_requests.get(
            self.url,
            response_type='status'
        )

    def _prepare_message(self) -> str:
        return f"{self._message_header}Response code: {self.status_code}"
