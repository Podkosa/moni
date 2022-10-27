from fastapi import APIRouter, Depends, Request

import checkers
from bot.integrations import slack, auth

router = APIRouter(prefix='/slack', dependencies=[Depends(auth.slack_key_verification)])

@router.post('/')
async def slack_request(request: Request):
    """Main slack endpoint"""
    return await slack.process_request(request)
