from fastapi import APIRouter, Depends, Request

from . import main, auth


router = APIRouter(prefix='/slack', dependencies=[Depends(auth.slack_signing_secret_validation)])


@router.post('/')
async def slack_request(request: Request):
    """Main slack endpoint. Slash commands map to endpoints in web.endpoints.check."""
    return await main.process_request(request)
