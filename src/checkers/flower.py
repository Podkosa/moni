import aiohttp, asyncio
from fastapi import HTTPException

from .abstract import Checker
from util import aio_requests, messages
import settings
from settings import logger


class FlowerChecker(Checker):
    options: dict = settings.CHECKERS['flower']['options']

    def __init__(self, user: str, password: str, *args, include_normal: bool = False, **kwargs):
        self.user = user
        self.password = password
        self.include_normal = include_normal
        super().__init__(*args, **kwargs)    

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
            'host': self.host,
            'status': status,
            'message': message
        }
        return self.result

    async def _get_data(self):
        self.response = await aio_requests.get(
            f'https://{self.host}{self.port if self.port else ""}/flower/api/queues/length',
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
            _host = f"Host: {self.host}"
            _queue = f"Queue: {queue['name']}"
            _messages = f"Messages: {queue['messages']}"
            queue_states.append('\n'.join((_host, _queue, _messages)))
        return '\n\n'.join(queue_states)

    @classmethod
    async def check_hosts(cls, hosts: list[str] | None = None) -> list[dict]:
        servers = settings.CHECKERS.get('flower', {}).get('servers')
        if not servers:
            raise HTTPException(500, 'Flower checker is not properly configured')

        if hosts:
            try:
                hosts_to_check = {host: servers.pop(host) for host in hosts}
            except KeyError as e:
                raise HTTPException(400, f'Unknown host {e.args[0]}')
        else:
            hosts_to_check = servers

        tasks = (cls(host=host, include_normal=True, **params).check() for host, params in hosts_to_check.items())
        return await asyncio.gather(*tasks)
