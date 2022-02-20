import paramiko
from dataclasses import dataclass


@dataclass(frozen=True)
class Output:
    '''
    Dataclass for command execution details and outputs
    '''
    ssh_id: str
    cmd: str
    cmd_status: int
    cmd_output: str
    cmd_error: str

    def get_ssh_id(self) -> str:
        return self.ssh_id

    def get_command(self) -> str:
        return self.cmd

    def get_status(self) -> int:
        return self.cmd_status

    def get_output(self) -> str:
        return self.cmd_output

    def get_error(self) -> str:
        return self.cmd_error


class SSH:
    '''
    SSH Connection and command execution.
    '''

    def __init__(self, hostname: str, username: str, port=22) -> None:
        self.__ssh_id = f'{username}@{hostname}'

        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()
        try:
            self._client.connect(
                hostname=hostname,
                username=username,
                port=port
            )
        except paramiko.SSHException as e:
            print(f'Failed while connecting the host: {self.__ssh_id}')
            print(str(e))
            exit(1)

    def command(self, command) -> Output:
        'Execute the command on the hosts'
        try:
            _, stdout, stderr = self._client.exec_command(
                command)
        except paramiko.SSHException as e:
            print(f'Failed while executing command: {self.__ssh_id}')
            print(str(e))
            exit(2)

        return Output(
            self.__ssh_id,
            command,
            stdout.channel.recv_exit_status(),
            stdout.read().decode('utf8'),
            stderr.read().decode('utf8')
        )

    def command_stream(self, command) -> None:
        'Execute command and print line wise'
        _, stdout, _ = self._client.exec_command(command)
        while True:
            line = stdout.readline()
            if not line:
                break
            print(line, end="")

    def close(self) -> None:
        'Close SSH connection'
        self._client.close()
