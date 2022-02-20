from click import echo, secho
import sys
import time
import threading


def ssh_id(id: str) -> None:
    'Show ssh_id'
    secho(
        f" 🧈 {id} ",
        bold=True,
        bg='cyan',
        nl=False
    )


def command(cmd: str) -> None:
    'Show command'
    secho(
        f"\t `$ {cmd}` \t",
        bg='white',
        fg='black',
        italic=True
    )


def command_output(output):
    'Show command output from `Output` dataclass object'

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
        self._control = True
        self._status = ' '
        self._clear = ' '
        self._max_r_len = 1

    def set_status(self, status: str) -> None:
        'Set current progress status'
        self._status = status
        if len(self._status) > self._max_r_len:
            self._max_r_len = len(self._status)
            self._clear = ' '*self._max_r_len

    def __loading(self) -> None:
        'Show loader'
        while self._control:
            sys.stdout.write(f'\r{self._status} | {self._clear}')
            time.sleep(0.1)
            sys.stdout.write(f'\r{self._status} / {self._clear}')
            time.sleep(0.1)
            sys.stdout.write(f'\r{self._status} - {self._clear}')
            time.sleep(0.1)
            sys.stdout.write(f'\r{self._status} \\ {self._clear}')
            time.sleep(0.1)
        sys.stdout.write(f'\r {self._clear} \n')

    def start(self) -> None:
        'Start loader'
        self._control = True
        self._loader_thread = threading.Thread(target=self.__loading)
        self._loader_thread.start()

    def stop(self) -> None:
        'Stop loader'
        self._control = False
        self._loader_thread.join()
