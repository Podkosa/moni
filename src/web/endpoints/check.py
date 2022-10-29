import asyncio

from fastapi import APIRouter, Query

import checkers


router = APIRouter(prefix='/check')


@router.post('/full_check/')
async def full_check():
    return await checkers.full_check()

@router.get('/ping/')
async def ping(hosts: list[str] | None = Query(default=None)) -> list[dict]:
    """Ping servers. Can handle arbitrary host, not defined in checkers.ping.servers."""
    return await checkers.PingChecker.check_hosts_with_unknown(hosts)

# Flower
@router.get('/celery/')
async def celery(hosts: list[str] | None = Query(default=None)) -> list[dict]:
    """Workers status and queues size"""
    return await checkers.FlowerChecker.check_workers(hosts)

@router.get('/workers/')
async def workers(hosts: list[str] | None = Query(default=None)) -> list[dict]:
    """Workers status"""
    return await checkers.FlowerChecker.check_workers(hosts)

@router.get('/queues/')
async def queues(hosts: list[str] | None = Query(default=None)) -> list[dict]:
    """Queues size"""
    return await checkers.FlowerChecker.check_queues(hosts)
