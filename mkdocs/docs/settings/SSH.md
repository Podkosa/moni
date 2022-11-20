Some checkers (like **DockerChecker**) use SSH. Configure your SSH access from Moni host to your servers as normal, then mount `.ssh/` directory to Moni container through a volume.

~~~~ YAML title="docker-compose.yml"
services:
  moni:
    volumes:
    - '~/.ssh/:/root/.ssh:ro'
~~~~

## UNIX permissions
Make sure that you set UNIX ownership/permissions, so that Moni container can read it.
~~~~ Bash
chown root:$USER ~/.ssh/config
chmod 644 ~/.ssh/config
ssh-add -k ~/.ssh/id_rsa
~~~~

## SSH Config file
Recommend you to get familiar with `.ssh/config` and how to pre-set aliases for your connections. Moni accepts `Host` aliases as server's `host` setting and will use it's configs for connections. This is the recommended way.

~~~~ title="config"
Host host_alias
  HostName your.host.com # or IP
  User root
  IdentityFile ~/.ssh/some_key.pub
~~~~
~~~~ YAML title="settings.yml"
checkers:
  docker:
    servers:
      host_alias:
~~~~
