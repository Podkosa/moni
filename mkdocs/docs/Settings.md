Main concept behind Moni is simplicity. For that, it uses declarative YAML settings.<br>
Choose from Checkers, Handlers and Integrations, cherry-pick what you like, set up a Watchdog and you're ready to go.<br>
Consult with `example.settings.yml` or follow up with an example below.

## Example
Let's say we need check every 5 seconds that [podkosa.github.io/moni/](https://podkosa.github.io/moni/) is up and returns a `2xx` response. 
And if something is wrong, let's alert to standard `STDOUT`. Looks simple enough! For that we consulted our *Moni Handbook* and found a **PingChecker** and a **ConsoleHandler**.<br>
Let's create a `settings.yml` file in the project directory and fill it as we go.

!!! warning "Security"
    This file will include your sensitive data, so be sure to take security measures.

!!! info "Containerization"
    If you're deploying inside a container (e.g. Docker), be sure to mount `./settings.yml:/moni/settings.yml` through `volumes`.

### API key
Bot endpoints are protected with an API key. Pass it as a cookie, header or query parameter named `access_token` with you requests to Moni.

~~~~ YAML title="settings.yml"
api_key: key
~~~~

!!! info "Integrations"
    Various integrations *(like Slack and Telegram)* use their own authentications methods and are not dependent on the Moni API key.
    Consult **Integrations** section for more info.

### Checker
~~~~ YAML title="settings.yml"
checkers:
  ping:
    servers:
      host1.com:
        endpoint: path/to/ping/
        protocol: 'https'
        cycle: 300
        handlers: [console]
~~~~
Here we have a basic configurations of a **Checker**. Top level `checkers` must include named **Checkers**. For our example we chose a **PingChecker**, so
we defined `ping`.<br>
Next we need to define our `servers`. They consist of key:value pairs that represent `host:config`.
Basic parameters, that are shared across all checkers are `cycle`, `handlers`, `protocol`, `port`.

-   `cycle`: `integer | float`<br>
    Seconds to wait between checks. Defaults to 300 seconds or 5 minutes. 
!!! info "Precision"
    Since Moni relies heavily on asynchronicity, this is implemented as a sleep between checks. For that, `cycle` is not absolute and may be slightly delayed
    by other running code.

-   `handlers`: `list[str]`<br>
    List of handlers, through which alerts will be sent. For example `[console, log, slack]` will output to `STDOUT`, write to `./logs/moni.log`
    and send a message to a *Slack* channel. Those 3 **Handlers** would have to be explicitly defined in the settings as well. 

-   `protocol`: `http`, `https`<br>
    Protocol to use for the requests. Defaults to `https`. 

-   `port`: `int`<br>
    Port to use for the requests. Defaults to not `None`, so 443(HTTPS) or 80(HTTP) is used. 

### Handler
Now let's define a **Handler**, so Moni knows how to alert you if something goes wrong. For this example we keep it simple and just print out to `STDOUT` with **ConsoleHandler**, so we simple defined `console`. This simple handler doesn't require additional settings, so let's move on.
~~~~ YAML title="settings.yml"
handlers:
  console:
~~~~

### Watchdog
With all of the above set, we have one last step to take (or rather one last :bone: to throw). Defining our :dog: **Watchdog**, that will run our checks periodically.
~~~~ YAML title="settings.yml"
watchdog:
  integrated: true
~~~~
!!! info "Watchdog"
    Consult **Watchdog** section for more details on this good pupper.

### Starting up Moni
All set! Just start up Moni and you'll see something like:
~~~~ console
INFO:     Started server process [1]
INFO:     Waiting for application startup.
Watchdog is running
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
~~~~
Moni is up and Watchdog is already running your checks. When our host will not response, you'll see a message with details on what went wrong.
~~~~ console
2022-10-31 12:00:00 PingChecker(podkosa.github.io) Cannot connect to host podkosa.github.io:443 ssl:default [Name or service not known]
2022-10-31 12:05:00 PingChecker(podkosa.github.io) 404, message='Not Found', url=URL('https://podkosa.github.io/moni/')
...
~~~~

### Logging
If you want to make sure that you've set everything correctly and checks are actually running, you can set Moni internal logging level from default `info` to `debug`.
~~~~ YAML title="settings.yml"
logger_level: debug
~~~~
And see something like:
~~~~ console
Running PingChecker(podkosa.github.io)
Finished PingChecker(podkosa.github.io)
~~~~
