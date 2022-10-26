import os, logging, sys
import aiohttp
from fastapi.logger import logger

### General ###
API_KEY = os.getenv('API_KEY')                                              # Access to all bot endpoints (header/cookie/query_param). Mandatory setting.
DEFAULT_REQUEST_TIMEOUT = aiohttp.ClientTimeout(
    total=int(os.getenv('REQUEST_TIMEOUT', 10))
)

### Logging ###
logger.handlers = [logging.StreamHandler(sys.stdout)]
logger.setLevel(logging.INFO)

### Handlers ###
# Slack
SLACK_HOST = ''
SLACK_PORT = int(os.getenv('SLACK_PORT', 1))
SLACK_USER = os.getenv('SLACK_USER', '')
SLACK_PASSWORD = os.getenv('SLACK_PASSWORD', '')

HANDLERS = {
    'slack': {
        'host': SLACK_HOST,
        'port': SLACK_PORT,
        'username': SLACK_USER,
        'password': SLACK_PASSWORD
    }
}

### Checkers ###
# Flower
# Currently only broker queues size
FLOWER_HOSTS = os.getenv('FLOWER_HOSTS', '').split(' ')
FLOWER_USER = os.getenv('FLOWER_USER', '')                                  # If you have different user/passwords in your flower instances,
FLOWER_PASSWORD = os.getenv('FLOWER_PASSWORD', '')                          # you can set them manually in CHECKERS.
QUEUE_MESSAGES_THRESHOLD = int(os.getenv('QUEUE_MESSAGES_THRESHOLD', 100))  # Alert if queue size is equal or greater

CHECKERS = {
    'flower': {
        'handlers': ['slack'],
        'servers': {
            host: {
                'username': FLOWER_USER,
                'password': FLOWER_PASSWORD
            }
        for host in FLOWER_HOSTS}
    } 
}

### Watchdog ###
WATCHDOG_ON_BOT_STARTUP = bool(os.getenv('WATCHDOG_ON_BOT_STARTUP', True))  # Start Watchdog inside Bot async event loop. May impact performance.
WATCHDOG_CYCLE = int(os.getenv('WATCHDOG_CYCLE', 300))                      # Seconds
