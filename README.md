# Moni

<p align="center">
<a href="https://podkosa.github.io/moni/"><img src="https://repository-images.githubusercontent.com/557768275/6a8a5d08-dc4f-4c19-9466-024af5c4d828"></a>
<br>
<em>a monitoring bot for your servers</em>
</p>

**Current features:**

- :robot: Bot: HTTP-server for on-demand checks
- :dog: Watchdog: Compact daemon for monitoing and alerting
- :mag: Checkers: Ping, Celery/Flower
- :loudspeaker: Handlers: Slack, Webhook, Log, Console
- :speech_balloon: Slack integration
- :fire: Speed: Async requests, Python 3.11, uvloop and FastAPI ensure the max gauge of your *Python* 
speedometer
- :hibiscus: Settings: Declarative YAML. Fine tune to your liking or fire-and-forget.
- :whale2: Docker: Pull the latest image from <a href="https://hub.docker.com/repository/docker/podkosa/moni" title="DockerHub">podkosa/moni</a>
- :notebook: Docs: Interactive docs at /docs

## Bot

HTTP server, handling incoming requests (REST, slash commands, integrations, webhooks etc.). On-demand checks.

## Watchdog

Periodically monitors servers with Checkers and alerts through Handlers.
Can be run in two ways:

1) Integrated (default).
Launch inside the bot async event loop. *Keep in mind thath they both will share a single thread, therefore can impact performance and even block one another.*
More compact option, but not fit for scaling.
2) Standalone.
Run ./watchdog.py as a separate process/container, even without the bot.
3) Disabled.
You can turn off the watchdog completely and run checks from the bot at your own pace.

## Settings

Define your servers, handlers, integrations and other settings declaratively in `settings.yml`. See `example.settings.yml`.
This file will include your sensetive data, so be sure to take security measures.
If you're deploying inside a container (e.g. Docker Compose), be sure to mount `./settings.yml:/botapp/settings.yml` through `volumes`.

## Integrations

Slack: alerts to channels and slash commands. Install Moni in your Workspace with `./integrations_docs/slack_app_manifest.yml`.

## TODO

- Telegram integration
- Email handler
- Remember previous alerts for subsequent checks, "back to normal" optional messages
- Alert when X is not normal for more than N time
- Slack timeout for /commands is 3 seconds. Refactor to delay the response.
- Slack button on an alert to open up related service
- Web interface for settings and checks
- Endpoint to show loaded checkers and handlers
- Endpoint to add servers to monitoring, turn on/off already configured ones
- Flower failed tasks alert?
- More alert handlers
- More server checkers
- More slash commands and REST options
- Customisable checker (get response from server, parse it in some way, figure out the status)
- Optional mutiprocessing, when there will be more checkers
- Tests
