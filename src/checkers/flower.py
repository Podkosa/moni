import aiohttp, asyncio

from conf import settings
from conf.settings import logger
from .abstract import Checker
from util import aio_requests, messages


_ENDPOINTS = {
    'flower': 'flower/api',
    'queues': '/queues',
    'length': '/length'
}

class FlowerChecker(Checker):
    name = 'flower'

    def __init__(self, user: str, password: str, *args, **kwargs):
        self.user = user
        self.password = password
        self.options: dict = settings.CHECKERS['flower'].get('options')
        if not self.options:
            raise settings.SettingsError(f'No options defined for {self.name} checker')
        super().__init__(*args, **kwargs)    

    async def check(self) -> dict:
        try:
            await self._get_data()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.debug(f"Couldn't check Flower on {self.host}: {e.__class__.__name__} {str(e)}")
            status = False
            message = messages.prepare_error_message(self, e)
        else:
            self._parse_data()
            status = all(map(lambda queue: queue['is_normal'], self.data['queues']))
            message = self._prepare_message()

        self.result = {
            'host': self.host,
            'status': status,
            'message': message
        }
        return self.result

    async def _get_data(self):
        self.response = await aio_requests.get(
            self.url + _ENDPOINTS['flower'] + _ENDPOINTS['queues'] + _ENDPOINTS['length'],
            auth=aiohttp.BasicAuth(self.user, self.password)
        )

    def _parse_data(self):
        self.data = {
            'queues': []
        }
        for queue in self.response['active_queues']:
            queue['is_normal'] = self._is_queue_normal(queue)
            self.data['queues'].append(queue)

    def _is_queue_normal(self, queue:dict) -> bool:
        return queue['messages'] < self.options['queues']['messages_threshold']

    def _prepare_message(self) -> str:
        queue_states = []
        for queue in self.data['queues']:
            if not self.include_normal and queue['is_normal']:
                continue
            _queue = f"Queue: {queue['name']}"
            _messages = f"Messages: {queue['messages']}"
            queue_states.append('\n'.join((_queue, _messages)))
        return self._message_header + '\n'.join(queue_states)
