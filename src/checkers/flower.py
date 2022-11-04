import aiohttp, asyncio

from conf import settings
from conf.settings import logger
from .abstract import Checker
from util import aio_requests, messages


_ENDPOINTS = {
    'flower': 'flower/api',
    'queues': '/queues/length',
    'workers': '/workers'
}

class FlowerChecker(Checker):
    name = 'flower'

    def __init__(self,
        user: str,
        password: str,
        options: dict = settings.CHECKERS.get('flower', {}).get('options', {}),
        *args,
        **kwargs
        ):
        self.user = user
        self.password = password
        self.options = options
        if not self.options or not ('queues' in self.options or 'workers' in self.options):
            raise settings.SettingsError(f'No options defined for {self.name} checker')
        if (queues := self.options.get('queues')) and not queues.get('size_threshold'):
            raise settings.SettingsError(f'No size_threshold for queues defined for {self.name} checker')
        super().__init__(*args, **kwargs)

    async def check(self) -> dict:
        try:
            await self._get_data()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.debug(f"Couldn't check Flower on {self.host}: {e.__class__.__name__} {str(e)}")
            status = False
            message = messages.prepare_error_message(self, e)
        else:
            status = self._parse_data()
            message = self._prepare_message()
        self.result = {
            'host': self.host,
            'check': self.name,
            'status': status,
            'message': message
        }
        return self.result

    @classmethod
    async def check_queues(cls, hosts: list[str] | None = None) -> list[dict]:
        hosts_to_check = cls._parse_hosts(hosts)
        default_options: dict = settings.CHECKERS['flower'].get('options', {})
        options = {}
        if 'queues' in default_options:
            options['queues'] = default_options['queues']
        tasks = (cls(
            host=host,
            include_normal=True,
            options=options,
            **params
        ).check() for host, params in hosts_to_check.items())
        return await asyncio.gather(*tasks)

    @classmethod
    async def check_workers(cls, hosts: list[str] | None = None) -> list[dict]:
        hosts_to_check = cls._parse_hosts(hosts)
        default_options: dict = settings.CHECKERS['flower'].get('options', {})
        options = {}
        if 'workers' in default_options:
            options['workers'] = default_options['workers']
        tasks = (cls(
            host=host,
            include_normal=True,
            options=options,
            **params
        ).check() for host, params in hosts_to_check.items())
        return await asyncio.gather(*tasks)

    async def _get_data(self):
        tasks = []
        if 'queues' in self.options:
            tasks.append(self._get_queues())
        if 'workers' in self.options:
            tasks.append(self._get_workers())
        await asyncio.gather(*tasks)

    async def _get_queues(self):
        self._queues_response = await self._flower_request(_ENDPOINTS['queues'])

    async def _get_workers(self):
        self._workers_response = await self._flower_request(_ENDPOINTS['workers'], params={'status': 'true'})

    async def _flower_request(self, endpoint: str, params: dict | None = None):
        return await aio_requests.get(
            self.url + _ENDPOINTS['flower'] + endpoint,
            params=params,
            auth=aiohttp.BasicAuth(self.user, self.password)
        )

    def _parse_data(self) -> bool:
        self.data = {
            'queues': [],
            'workers': []
        }
        if hasattr(self, '_queues_response'):
            for queue in self._queues_response['active_queues']:
                queue['is_normal'] = self._is_queue_normal(queue)
                self.data['queues'].append(queue)
        if hasattr(self, '_workers_response'):
            for worker, status in self._workers_response.items():
                self.data['workers'].append({'name': worker, 'is_normal': status})
        return all(map(lambda i: i['is_normal'], self.data['queues'] + self.data['workers']))

    def _is_queue_normal(self, queue:dict) -> bool:
        return queue['messages'] < self.options['queues']['size_threshold']

    def _prepare_message(self) -> str:
        sub_messages = []
        for worker in self.data['workers']:
            if not self.include_normal and worker['is_normal']:
                continue
            _worker = f"Worker: {worker['name']}"
            _status = f"Status: {'Up' if worker['is_normal'] else 'Down'}"
            sub_messages.append('\n'.join((_worker, _status)))
        for queue in self.data['queues']:
            if not self.include_normal and queue['is_normal']:
                continue
            _queue = f"Queue: {queue['name']}"
            _messages = f"Messages: {queue['messages']}"
            sub_messages.append('\n'.join((_queue, _messages)))
        return self._message_header + '\n'.join(sub_messages)
