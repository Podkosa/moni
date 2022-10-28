from conf import settings
from .abstract import Handler, HandlerError
from util import aio_requests


class SlackHandler(Handler):
    url = settings.HANDLERS['slack'].get('webhook_url')

    async def _send_message(self, message: str):
        if not self.url:
            raise HandlerError('slack.webhook_url is not set')
        data = {'text': message}
        return await aio_requests.post(self.url, data, response_type='text')
