<p align="center">
<b>Moni</b>
<br>
<em>a monitoring bot for your servers</em>
</p>

**Current features:**

- Monitor Celery broker queues size (through Flower API)
- Autonomous watchdog
- REST interface

**Watchdog:**
Periodically monitors servers and alert. See settings.py for possible configurations of servers Checkers and alert Handlers.
Can be run in two ways:

1) Integrated (default).
The watchdog will launch inside the bot async event loop. Keep in mind thath they both will share a single thread, therefore can impact performance and even block one-another.
More compact option, but not fit for scaling.
2) Standalone.
You can run ./checkers/watchdog.py as a separate process/container.

**Settings:**
Easiest way is through environmental variables. See sample.env for a full list.
For example, if you're running the server with Docker Compose, define a .env file near the docker-compose.yml.
Alternatevly you can write your own settings.py file and mount it directly to /botapp/settings.py inside the container.

**TODO:**

- Slack integration (Handler for alerts and run commands from Slask)
- Telegram integration (same)
- Parse checkers and handlers settings from .yml file
- Check if docs are protected by API key
- Tests
