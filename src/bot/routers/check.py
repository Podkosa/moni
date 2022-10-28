from fastapi import APIRouter

import checkers


router = APIRouter(prefix='/check')


@router.post('/all')
async def check_all():
    #TODO: optionally run in the background
    await checkers.check_all()

@router.get('/queues')
async def queues(hosts: list[str] | None = None) -> list:
    """Current queues size"""
    return await checkers.FlowerChecker.check_hosts(hosts)
