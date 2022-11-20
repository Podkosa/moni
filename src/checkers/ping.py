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

    async def _get_data(self):
        self.status_code = await aio_requests.get(
            self.url + (self.endpoint if self.endpoint else ''),
            response_type='status'
        )

    def _parse_data(self) -> bool:
        # _get_data() will raise Exceptions if status code is not 200 and `False` status would be set there
        return True

    def _prepare_message(self) -> str:
        return f"{self._message_header}Response code: {self.status_code}"

    @classmethod
    async def check_hosts_with_unknown(cls, hosts: list[str] | None = None) -> list[dict]:
        if not hosts:
            results = await cls.check_hosts(hosts)
        else:
            known_hosts, unknown_hosts = cls.extract_unknown_hosts(hosts)
            results = []
            if known_hosts:
                results +=  await cls.check_hosts(known_hosts)
            if unknown_hosts:
                unknown_pings = []
                for unknown_host in unknown_hosts:
                    parsed = unknown_host.split('/', 1)
                    host = parsed.pop(0)
                    endpoint = parsed[0] if parsed else None
                    checker = cls(host=host, endpoint=endpoint)
                    unknown_pings.append(checker.check())
                results += await asyncio.gather(*unknown_pings)
        return results
