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

**Bot:**

HTTP server, handling incoming requests (REST, slash commands, integrations, webhooks etc.). Can check on-demand and return the results or launch a full check in the background with standard alerts.

**Watchdog:**

Periodically monitors servers with Checkers and alerts through Handlers. See `settings.yml` for possible configurations.
Can be run in two ways:

1) Integrated (default).
Watchdog will launch inside the bot async event loop. Keep in mind thath they both will share a single thread, therefore can impact performance and even block one another.
More compact option, but not fit for scaling.
2) Standalone.
You can run ./watchdog.py as a separate process/container.

**Settings:**

Define your servers, handlers, integrations and other settings declaratively in `settings.yml`. See `example.settings.yml`.
Set environmental variables `API_KEY` and `BOT_PORT` for the bot. See `example.env`.

If you're deploying inside a container (e.g. Docker Compose), be sure to mount `./settings.yml:/botapp/settings.yml` through `volumes` and set env variables through `env_file`.

**TODO:**

- Telegram integration
- File and stdout handler
- Remember previous alerts for subsequent checks, "back to normal" optional messages
- Slack app distribution or manifest
- More alert handlers
- More server checkers
- More slash commands and REST options
- Tests
