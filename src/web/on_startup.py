import asyncio

from conf import settings
import watchdog


class SettingsError(Exception):
    pass


def verify_settings():
    if not settings.API_KEY:
        raise SettingsError('API_KEY is not set')

async def set_up():
    verify_settings()
    if settings.WATCHDOG.get('integrated'):
        asyncio.create_task(watchdog.watch())
