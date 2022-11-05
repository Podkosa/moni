Checks workers status and queues sizes of your **Celery** server through **Flower** endpoints `flower/api/workers` and `flower/api/queues/length`.

~~~~ YAML title="settings.yml"
checkers:
  flower:
    options:
      queues:
        size_threshold: 100
      workers:
    servers:
      host1.com:
        endpoint: path/to/ping/
        user: user1
        password: password1
        # handlers: [...]
        # cycle: 300
~~~~
