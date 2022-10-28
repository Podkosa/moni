from fastapi import FastAPI, Depends

from conf import settings
from .endpoints import check
from . import on_startup, auth, integrations


app = FastAPI()
app.include_router(check.router, dependencies=[Depends(auth.api_key_auth)])
for integration in settings.INTEGRATIONS:
    module = getattr(integrations, integration)
    print(module.__dict__)
    app.include_router(module.endpoints.router)


@app.on_event('startup')
async def set_up():
    await on_startup.set_up()

@app.get('/ping')
def ping() -> str:
    return 'Pong!'
