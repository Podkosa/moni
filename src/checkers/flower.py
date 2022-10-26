import aiohttp, asyncio
from dataclasses import dataclass

from .abstract import Checker
from util import aio_requests, messages
import settings
from settings import logger

@dataclass
class FlowerChecker(Checker):
    include_normal_queues: bool = False

    async def check(self) -> dict:
        try:
            await self._get_data()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.warning(f"Couldn't check Flower on host {self.host}", exc_info=e)
            status = False
            message = messages.prepare_error_message(e)
        else:
            self._parse_data()
            status = all(map(lambda queue: queue['is_normal'], self.data['queues']))
            message = self._prepare_message()

        self.result = {
            'status': status,
            'message': message
        }
        return self.result

    async def _get_data(self):
        self.response = await aio_requests.get(
            f'https://{self.host}/flower/api/queues/length',
            auth=aiohttp.BasicAuth(settings.FLOWER_USER, settings.FLOWER_PASSWORD)
        )
        self.json = await self.response.json()

    def _parse_data(self):
        self.data = {
            'queues': []
        }
        for queue in self.json['active_queues']:
            queue['is_normal'] = self._is_queue_normal(queue)
            self.data['queues'].append(queue)

    def _is_queue_normal(self, queue:dict) -> bool:
        return queue['messages'] >= settings.QUEUE_MESSAGES_THRESHOLD

    def _prepare_message(self) -> str:
        queue_states = []
        for queue in self.data['queues']:
            if not self.include_normal_queues and queue['is_normal']:
                continue
            _host = f"Host: {self.host.split('.')[0]}"
            _queue = f"Queue: {queue['name']}"
            _messages = f"Messages: {queue['messages']}"
            queue_states.append('\n'.join((_host, _queue, _messages)))
        return '\n'.join(queue_states)
