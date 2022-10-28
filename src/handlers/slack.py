from .abstract import Handler
from .utils import CheckerError
from util import aio_requests
import settings


class SlackHandler(Handler):
    async def handle(self, message: str):
        url = settings.HANDLERS['slack']['webhook_url']
        if not url:
            raise CheckerError('slack.webhook_url is not set')
        data = {'text': message}
        return await aio_requests.post(url, data, response_type='text')
