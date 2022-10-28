import hmac, hashlib
from fastapi import HTTPException, Request
from starlette.status import HTTP_403_FORBIDDEN

from conf import settings


async def slack_signing_secret_validation(request: Request):
    slack_signing_secret = settings.INTEGRATIONS['slack']['signing_secret']
    timestamp = request.headers['X-Slack-Request-Timestamp']
    request_body = await request.body()
    request_body = request_body.decode("utf-8")
    sig_basestring = 'v0:' + timestamp + ':' + request_body
    signature = 'v0=' + hmac.new(slack_signing_secret.encode(), sig_basestring.encode(), hashlib.sha256).hexdigest()
    if hmac.compare_digest(signature, request.headers['X-Slack-Signature']):
        return request
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Could not validate Slack Signing Secret')

