Basic **Checker** that sends an HTTP GET request to your server and alerts if the response is `4**`, `5**` or if it couldn't connect. Can do basic user-password authentication.

~~~~ YAML title="settings.yml"
checkers:
  ping:
    servers:
      host1.com:
        endpoint: path/to/ping/
        # user: user1
        # password: password1
        # handlers: [...]
        # cycle: 300
~~~~
