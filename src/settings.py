import os, logging, sys
import aiohttp, yaml
from fastapi.logger import logger


### Logging ###
logger.handlers = [logging.StreamHandler(sys.stdout)]
logger.setLevel(logging.INFO)

### General ###
yml: dict = yaml.safe_load(open('settings.yml'))

API_KEY = os.getenv('API_KEY')
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=yml.get('request_timeout'))

### Checkers ###
CHECKERS = yml.get('checkers', {})
# Flower
for host in CHECKERS.get('flower', {}).get('servers', {}):
    if (params := CHECKERS['flower']['servers'][host]) is None:
        params = CHECKERS['flower']['servers'][host] = {}
    params.setdefault('user', CHECKERS['flower'].get('default').get('user'))
    params.setdefault('password', CHECKERS['flower'].get('default').get('password'))
    params.setdefault('port', CHECKERS['flower'].get('default').get('port'))

### Handlers ###
# Slack
HANDLERS = yml.get('handlers', {})

### Integrations ###
INTEGRATIONS = yml.get('integrations', {})

### Watchdog ###
WATCHDOG = yml.get('watchdog', {})
