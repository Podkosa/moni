from conf import settings
from .abstract import Handler, HandlerError
from util import aio_requests


class SlackHandler(Handler):
    def __init__(self):
        self.url = settings.HANDLERS['slack']['webhook_url']

    async def _send_message(self, message: str):
        data = {'text': message}
        return await aio_requests.post(self.url, data, response_type='text')
