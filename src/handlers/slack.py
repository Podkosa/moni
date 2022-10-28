from conf import settings
from .abstract import Handler, HandlerError
from util import aio_requests


class SlackHandler(Handler):
    async def handle(self, message: str):
        url = settings.HANDLERS['slack']['webhook_url']
        if not url:
            raise HandlerError('slack.webhook_url is not set')
        data = {'text': message}
        return await aio_requests.post(url, data, response_type='text')
