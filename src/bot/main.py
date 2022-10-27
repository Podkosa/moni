from fastapi import FastAPI, Depends

from .routers import check, slack
from .auth import api_key_auth
from . import on_startup

app = FastAPI()
app.include_router(check.router, dependencies=[Depends(api_key_auth)])
app.include_router(slack.router)

@app.on_event('startup')
async def set_up():
    await on_startup.set_up()

@app.get('/ping')
def ping():
    return 'Pong!'

# @app.get('/help')
# def help():
#     return """Commands:
# /check/queues   Get queues size
# /check/all      Run a full check with standard alerts
# """
