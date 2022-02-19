import paramiko


class SSH:
    '''
    SSH Connection and command execution.
    '''

    def __init__(self, hostname: str, username: str, port=22) -> None:
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(hostname=hostname, username=username, port=port)
        self.cmd_output = self.Output(hostname, username)

    def command(self, command) -> object:
        _, stdout, stderr = self.client.exec_command(
            command)
        self.cmd_output.cmd = command
        self.cmd_output.cmd_status = stdout.channel.recv_exit_status()
        self.cmd_output.cmd_output = stdout.read().decode('utf8')
        self.cmd_output.cmd_error = stderr.read().decode('utf8')

        return self.cmd_output

    def command_stream(self, command) -> None:
        stdin, stdout, stderr = self.client.exec_command(command)
        while True:
            line = stdout.readline()
            if not line:
                break
            print(line, end="")

    def close(self) -> None:
        self.client.close()

    class Output:
        def __init__(self, hostname, username) -> None:
            self.ssh_id = f'{username}@{hostname}'
            self.cmd_status = 0
            self.cmd_output = ''
            self.cmd_error = ''
            self.cmd = ''

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
