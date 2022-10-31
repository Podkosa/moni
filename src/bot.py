from fastapi import FastAPI, Depends

from conf import settings
from web.endpoints import check
from web import auth, integrations, startup_shutdown


app = FastAPI()
app.include_router(check.router, dependencies=[Depends(auth.api_key_auth)])
for integration in settings.INTEGRATIONS:
    module = getattr(integrations, integration)
    app.include_router(module.endpoints.router)


@app.on_event('startup')
async def on_startup():
    await startup_shutdown.on_startup()

@app.on_event('shutdown')
async def on_shutdown():
    await startup_shutdown.on_shutdown()

@app.get('/ping')
def ping() -> str:
    """Basic bot healthcheck. Not to be confused with PingChecker for servers."""
    return 'Pong!'
