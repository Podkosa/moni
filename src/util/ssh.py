import asyncssh

from conf import settings

async def command(
    command: str,
    host: str,
    port: int = 22, # Standard SSH port
    timeout: int | float = settings.SSH_TIMEOUT
    ) -> str:
    """Run shh command on a remote host, return `stdout`"""
    try:
        async with asyncssh.connect(host=host, port=port, connect_timeout=timeout, passphrase=settings.SSH_PASSPHRASE) as conn:
            result = await conn.run(
                command,
                timeout=timeout,
                check=True
            )
            return str(result.stdout)
    except asyncssh.misc.PermissionDenied as e:
        e.add_note(f'Could not connect to SHH server {host}. Potential auth problems. Check if .ssh/config, permissions and ssh_passphrase (if needed) are correct.')
        raise e
