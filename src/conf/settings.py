import os, logging, sys
import aiohttp, yaml
from fastapi.logger import logger

from . import default_setters


### Logging ###
logger.handlers = [logging.StreamHandler(sys.stdout)]
logger.setLevel(logging.INFO)

### General ###
yml: dict = yaml.safe_load(open('settings.yml'))

API_KEY = os.getenv('API_KEY')
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=yml.get('request_timeout'))

### Watchdog ###
WATCHDOG = yml.get('watchdog', {})

### Checkers ###
CHECKERS = yml.get('checkers', {})

for checker, conf in CHECKERS.items():
    defaults = WATCHDOG.get('default', {}).copy()                               # Watchdog level defaults
    defaults.update(conf.get('default'))                                        # Checker level defaults
    for host, params in conf['servers'].items():
        if params is None:
            params = conf['servers'][host] = {}
        params.setdefault('handlers', defaults.get('handlers'))
        params.setdefault('cycle', defaults.get('cycle'))
        getattr(default_setters, checker, lambda *args: None)(params, defaults)    # Server level defaults

### Handlers ###
HANDLERS = yml.get('handlers', {})

### Integrations ###
INTEGRATIONS = yml.get('integrations', {})
