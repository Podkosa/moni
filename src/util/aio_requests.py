import aiohttp

import settings


async def get(url: str, params: dict | None = None, **kwargs) -> dict:
    return await request('GET', url, params=params, **kwargs)

async def post(url: str, data: dict, **kwargs) -> dict:
    return await request('POST', url, json=data, **kwargs)

async def request(method, url, **kwargs) -> dict:
    async with aiohttp.ClientSession(timeout=settings.DEFAULT_REQUEST_TIMEOUT, raise_for_status=True) as session:
        async with session.request(method, url, **kwargs) as resp:
            return await resp.json()
