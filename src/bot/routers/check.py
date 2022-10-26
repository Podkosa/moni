import asyncio

from fastapi import APIRouter, HTTPException

import checkers, settings

router = APIRouter(prefix='/check')

@router.post('/all')
async def check_all():
    await checkers.check_all()

@router.get('/queues')
async def queues(hosts: list[str] | None = None) -> str:
    """Current queues size"""
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

    tasks = (checkers.FlowerChecker(host=host, **params).check() for host, params in hosts_to_check.items())
    results = await asyncio.gather(*tasks)
    return '\n'.join((result['message'] for result in results))
