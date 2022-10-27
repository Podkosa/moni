from typing import Any

from fastapi import Request, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

import checkers

async def process_request(request: Request) -> Any:
    json = await request.form()
    match json['command']:
        case '/queues':
            text = json.get('text')
            hosts = text.split(' ') if text else None  # type: ignore
            results = await checkers.FlowerChecker.check_hosts(hosts)
            return prepare_check_response(results)
        case _:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Unknown command')

def prepare_check_response(results: list[dict]) -> dict:
    response = {
    "response_type": "in_channel",
    "text": '\n\n'.join((result['message'] for result in results))
    }
    return response
