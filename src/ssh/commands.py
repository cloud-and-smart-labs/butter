from src.inventory.inventory import Inventory
from src.ssh.ssh import SSH
from src.ssh.printer import *


def shell_command(inventory_name: str, cmd: str) -> None:
    loader = Loading()
    for host in Inventory(inventory_name).get_inventory_list():
        loader.start()

        loader.set_status('Connecting...')
        ssh_connection = SSH(host[0], host[1], port=int(host[2]))

        loader.set_status('Executing...')
        output = ssh_connection.command(cmd)

        loader.set_status('Done.')
        ssh_connection.close()

        loader.stop()
        command_output(output)
