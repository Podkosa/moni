from fastapi import APIRouter, Depends, Request

from bot.integrations import slack, auth


router = APIRouter(prefix='/slack', dependencies=[Depends(auth.slack_signing_secret_validation)])


@router.post('/')
async def slack_request(request: Request):
    """Main slack endpoint"""
    return await slack.process_request(request)
