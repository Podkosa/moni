<p align="center">
<img src="https://repository-images.githubusercontent.com/557768275/6a8a5d08-dc4f-4c19-9466-024af5c4d828">
<br>
<em>a monitoring bot for your servers</em>
</p>

**Current features:**

- Monitor Celery broker queues size (through Flower API)
- Autonomous watchdog
- Slack integration (alerts to channel and slash commands)
- REST interface
- Interactive docs at /docs

**Watchdog:**

Periodically monitors servers and alerts. See settings.py for possible configurations of servers Checkers and alert Handlers.
Can be run in two ways:

1) Integrated (default).
Watchdog will launch inside the bot async event loop. Keep in mind thath they both will share a single thread, therefore can impact performance and even block one another.
More compact option, but not fit for scaling.
2) Standalone.
You can run ./watchdog.py as a separate process/container.

**Settings:**

Easiest way is through environmental variables. See sample.env for a full list.
For example, if you're running the server with Docker Compose, define a .env file near the docker-compose.yml.
Alternatevly you can write your own settings.py file and mount it directly to /botapp/settings.py inside the container.

**TODO:**

- Telegram integration
- File and stdout handler
- More alert handlers
- More server checkers
- Define servers and alerts declaratively from a .yml file
- More slash commands and REST options
- Tests
