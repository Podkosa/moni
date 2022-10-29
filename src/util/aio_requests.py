from typing import Any
import aiohttp

from conf import settings


async def get(url: str, params: dict | None = None, **kwargs) -> dict:
    return await request('GET', url, params=params, **kwargs)

async def post(url: str, data: dict, **kwargs) -> dict:
    return await request('POST', url, json=data, **kwargs)

async def request(method, url, **kwargs) -> Any:
    response_type = kwargs.pop('response_type', 'json')
    async with aiohttp.ClientSession(timeout=settings.REQUEST_TIMEOUT, raise_for_status=True) as session:
        async with session.request(method, url, **kwargs) as resp:
            match response_type:
                case 'json':
                    return await resp.json()
                case 'text':
                    return await resp.text()
                case 'bytes':
                    return await resp.read()
                case 'status':
                    return resp.status
                case 'ignore':
                    return
                case _:
                    raise NotImplementedError
