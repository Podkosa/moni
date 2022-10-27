import asyncio
import settings, watchdog

class SettingsError(Exception):
    pass

def verify_settings():
    if not settings.API_KEY:
        raise SettingsError('API_KEY is not set')

async def set_up():
    verify_settings()
    if settings.WATCHDOG_ON_BOT_STARTUP:
        asyncio.create_task(watchdog.watch())
