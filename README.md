<p align="center">
<img src="https://repository-images.githubusercontent.com/557768275/6a8a5d08-dc4f-4c19-9466-024af5c4d828">
<br>
<em>a monitoring bot for your servers</em>
</p>

**Current features:**

- Bot (HTTP-server) for on-demand checks
- Autonomous compact watchdog for monitoing and alerting
- Slack integration: alerts to channel and slash commands
- Checks: Celery broker queues size (through Flower API) (working on more)
- Speed: Asynchronous requests, Python 3.11 and FastAPI ensure the max gauge of your *Python* 
speedometer.
- Declarative YAML settings
- Interactive docs at /docs

**Bot:**

HTTP server, handling incoming requests (REST, slash commands, integrations, webhooks etc.). Can check on-demand and return the results or launch a full check in the background with standard alerts.

**Watchdog:**

Periodically monitors servers with Checkers and alerts through Handlers.
Can be run in two ways:

1) Integrated (default).
Watchdog will launch inside the bot async event loop. *Keep in mind thath they both will share a single thread, therefore can impact performance and even block one another.*
More compact option, but not fit for scaling.
2) Standalone.
You can run ./watchdog.py as a separate process/container, even without the bot.
3) Disabled.
You can turn off the watchdog and run checks from the bot at your own pace.

**Settings:**

Define your servers, handlers, integrations and other settings declaratively in `settings.yml`. See `example.settings.yml`.
This file will include your sensetive data, so be sure to take security measures.
If you're deploying inside a container (e.g. Docker Compose), be sure to mount `./settings.yml:/botapp/settings.yml` through `volumes`.

**TODO:**

- Telegram integration
- Health/heartbeat/pings checker
- Customisable checker (get response from server, parse it in some way, figure out the status)
- File, email handler
- Remember previous alerts for subsequent checks, "back to normal" optional messages
- Slack app distribution or manifest
- More alert handlers
- More server checkers
- Optional mutiprocessing, when there will be more checkers
- More slash commands and REST options
- Tests
