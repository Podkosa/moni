from fastapi.security import api_key
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from conf import settings


key_name = 'access_token'
api_key_query = api_key.APIKeyQuery(name=key_name, auto_error=False)
api_key_header = api_key.APIKeyHeader(name=key_name, auto_error=False)
api_key_cookie = api_key.APIKeyCookie(name=key_name, auto_error=False)


def api_key_auth(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie)
    ):
    for key in (api_key_query, api_key_header, api_key_cookie):
        if key == settings.API_KEY:
            return key
    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Could not validate API KEY')
