import asyncssh

from conf.settings import logger
from .abstract import Checker
from util import ssh, messages


class DockerChecker(Checker):
    name = 'docker'
    _BAD_CONTAINER_STATES = {'exited', 'restarting', 'paused', 'dead'}

    async def check(self) -> dict:
        try:
            await self._get_data()
        except (asyncssh.misc.PermissionDenied, ) as e:
            logger.debug(f"Couldn't check Docker on {self.host}: {e.__class__.__name__} {str(e)}")
            status = False
            message = messages.prepare_error_message(self, e)
        else:
            status = self._parse_data()
            message = self._prepare_message()

        self.result = {
            'host': self.host,
            'check': self.name,
            'status': status,
            'message': message
        }
        return self.result

    async def _get_data(self):
        self._data = await ssh.command(
            command=r'docker ps --format "{{.Names}};{{.State}};{{.Status}}"',
            host=self.host,
            port=self.port  # type: ignore , will be set to 22 if not defined
        )

    def _parse_data(self) -> bool:
        self._containers = []
        for container in self._data.splitlines():
            self._containers.append(self._parse_container(container))
        if self._containers:
            return all(map(lambda i: i['is_normal'], self._containers))
        else:
            return False

    def _parse_container(self, container: str) -> dict:
        name, state, status = container.split(';')
        return {
            'name': name,
            'state': state,
            'status': status,
            'is_normal': state not in self._BAD_CONTAINER_STATES
        }

    def _prepare_message(self) -> str:
        if not self._containers:
            return self._message_header + f'No containers found'
        sub_messages = []
        for container in self._containers:
            if not self.include_normal and container['is_normal']:
                continue
            _container = f"Container: {container['name']}"
            _status = f"Status: {container['status']}"
            sub_messages.append('\n'.join((_container, _status)))
        return self._message_header + '\n'.join(sub_messages)
