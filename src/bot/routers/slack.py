from fastapi import APIRouter

import checkers
from bot.integrations import slack

router = APIRouter(prefix='/slack')

@router.post('/check/all')
async def check_all() -> None:
    await checkers.check_all()

@router.post('/check/queues')
async def queues(hosts: list[str] | None = None) -> dict:
    """Current queues size"""
    results = await checkers.FlowerChecker.check_hosts(hosts)
    response = slack.prepare_check_response(results)
    return response
