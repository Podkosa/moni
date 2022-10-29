from typing import Any

from fastapi import Request, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from web.endpoints import check


async def process_request(request: Request) -> Any:
    data = await request.form()
    command: str = data['command']  # type: ignore
    text: str = data.get('text')  # type: ignore
    arguments = text.split(' ') if text else None
    if endpoint := getattr(check, command, None):
        results = await endpoint(arguments)
        return prepare_response(results)
    else:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Unknown command')

def prepare_response(results: list[dict]) -> dict:
    response = {
    "response_type": "in_channel",
    "text": '\n\n'.join((result['message'] for result in results))
    }
    return response
