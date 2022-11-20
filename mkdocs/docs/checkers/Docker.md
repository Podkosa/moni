Checks Docker container status. Runs `docker ps --format ...` on your servers. Requires SSH (see **Settings/SSH**).

~~~~ YAML title="settings.yml"
checkers:
  docker:
    servers:
      host1.com:
        # port: 22
        # handlers: [...]
        # cycle: 300
      host2_alias:
~~~~
