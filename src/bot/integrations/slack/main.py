from typing import Any

from fastapi import Request, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

import checkers


async def process_request(request: Request) -> Any:
    data = await request.form()
    text = data.get('text')
    arguments = text.split(' ') if text else None  # type: ignore
    match data['command']:
        case '/queues':
            results = await checkers.FlowerChecker.check_hosts(arguments)
        case _:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Unknown command')
    return prepare_response(results)

def prepare_response(results: list[dict]) -> dict:
    response = {
    "response_type": "in_channel",
    "text": '\n\n'.join((result['message'] for result in results))
    }
    return response
