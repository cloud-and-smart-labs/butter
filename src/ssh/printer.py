from click import echo, secho
import sys
import time
import threading


def ssh_id(id: str) -> None:
    secho(
        f" 🧈 {id} ",
        bold=True,
        bg='cyan',
        nl=False
    )


def command(cmd: str) -> None:
    secho(
        f"\t `$ {cmd}` \t",
        bg='white',
        fg='black',
        italic=True
    )


def command_output(output):
    'Show command output from `Output` object'

    ssh_id(output.get_ssh_id())

    # Command status code
    secho(
        f" STATUS {output.get_status()} ",
        bold=True,
        bg='green',
        fg='white',
        nl=False
    ) if 0 == output.get_status(
    ) else secho(
        f" STATUS {output.get_status()} ",
        bold=True,
        bg='red',
        fg='white',
        nl=False
    )

    command(output.get_command())

    # Command output
    if 0 == output.get_status():
        echo(output.get_output())

    # Command error
    else:
        secho(
            output.get_error(),
            fg='red'
        )


class Loading:
    'Console based loader with live status'

    def __init__(self) -> None:
        self.control = True
        self.status = ' '
        self.clear = ' '
        self.max_r_len = 1

    def set_status(self, status: str) -> None:
        self.status = status
        if len(self.status) > self.max_r_len:
            self.max_r_len = len(self.status)
            self.clear = ' '*self.max_r_len

    def loading(self) -> None:
        while self.control:
            sys.stdout.write(f'\r{self.status} | {self.clear}')
            time.sleep(0.1)
            sys.stdout.write(f'\r{self.status} / {self.clear}')
            time.sleep(0.1)
            sys.stdout.write(f'\r{self.status} - {self.clear}')
            time.sleep(0.1)
            sys.stdout.write(f'\r{self.status} \\ {self.clear}')
            time.sleep(0.1)
        sys.stdout.write(f'\r {self.clear} \n')

    def start(self) -> None:
        self.control = True
        self.loader_thread = threading.Thread(target=self.loading)
        self.loader_thread.start()

    def stop(self) -> None:
        self.control = False
        self.loader_thread.join()
