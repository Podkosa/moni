import aiohttp

import settings


async def get(url: str, params: dict | None = None, **kwargs) -> aiohttp.ClientResponse:
    return await request('GET', url, params=params, **kwargs)

async def post(url: str, data: dict, **kwargs) -> aiohttp.ClientResponse:
    return await request('POST', url, json=data, **kwargs)

async def request(method, url, **kwargs) -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession(timeout=settings.DEFAULT_REQUEST_TIMEOUT, raise_for_status=True) as session:
        async with session.request(method, url, **kwargs) as resp:
            return resp
