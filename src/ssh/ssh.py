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
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(hostname=hostname, username=username, port=port)
        self.ssh_id = f'{username}@{hostname}'

    def command(self, command) -> Output:
        _, stdout, stderr = self.client.exec_command(
            command)

        return Output(
            self.ssh_id,
            command,
            stdout.channel.recv_exit_status(),
            stdout.read().decode('utf8'),
            stderr.read().decode('utf8')
        )

    def command_stream(self, command) -> None:
        stdin, stdout, stderr = self.client.exec_command(command)
        while True:
            line = stdout.readline()
            if not line:
                break
            print(line, end="")

    def close(self) -> None:
        self.client.close()
