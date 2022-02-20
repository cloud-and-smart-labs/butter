from src.inventory.inventory import Inventory
from src.ssh.ssh import SSH
from src.ssh.printer import *
import threading


def shell_command(inventory_name: str, cmd: str) -> None:
    'Shell command execute concurrently'

    def executor(host: list, output_lock: threading.Lock) -> None:
        'Shell command executor'
        loader = Loading()
        loader.start()

        try:
            loader.set_status(f'Connecting [{host[0]}] ...')
            ssh_connection = SSH(host[0], host[1], port=int(host[2]))

            loader.set_status(f'Executing [{host[0]}] ...')
            output = ssh_connection.command(cmd)

            loader.set_status(f'Done [{host[0]}] .')
            ssh_connection.close()
            loader.stop()

            with output_lock:
                # print(f'lock acquire by: {threading.current_thread()}')
                command_output(output)
                # print(f'lock release by: {threading.current_thread()}')

        except Exception as e:
            loader.stop()
            print(str(e))

    output_lock = threading.Lock()
    for host in Inventory(inventory_name).get_inventory_list():
        threading.Thread(name=host[0],
                         target=executor,
                         args=(host, output_lock),).start()


def shell_command_stream(inventory_name: str, cmd: str) -> None:
    'Command with -s (stream) switch'
    loader = Loading()
    for host in Inventory(inventory_name).get_inventory_list():
        loader.start()
        try:
            loader.set_status(f'Connecting [{host[0]}] ...')
            ssh_connection = SSH(host[0], host[1], port=int(host[2]))

            loader.set_status(f'Executing [{host[0]}] ...')
            loader.stop()
            ssh_id(f'{host[1]}@{host[0]}')
            command(cmd)

            ssh_connection.command_stream(cmd)
            ssh_connection.close()
        except Exception as e:
            loader.stop()
            print(str(e))
