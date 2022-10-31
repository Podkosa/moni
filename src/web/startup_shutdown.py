import asyncio

from conf import settings
import watchdog
import handlers

class SettingsError(Exception):
    pass


def verify_settings():
    if not settings.API_KEY:
        raise SettingsError('API_KEY is not set')

async def on_startup():
    verify_settings()
    if settings.WATCHDOG.get('integrated'):
        asyncio.create_task(watchdog.watch())
    for handler_name in settings.ON_STARTUP_HANDLERS:
        handler: handlers.Handler = handlers.get_handler_cls(handler_name)()
        await handler.handle({'message': f'Moni is up'})

async def on_shutdown():
    for handler_name in settings.ON_STARTUP_HANDLERS:
        handler: handlers.Handler = handlers.get_handler_cls(handler_name)()
        await handler.handle({'message': f"Moni is down"})
