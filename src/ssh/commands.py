from src.inventory.inventory import Inventory
from src.ssh.ssh import SSH
from src.ssh.printer import *


def shell_command(inventory_name: str, cmd: str) -> None:
    for host in Inventory(inventory_name).get_inventory_list():
        ssh_connection = SSH(host[0], host[1], port=int(host[2]))
        output = ssh_connection.command(cmd)
        ssh_connection.close()
        command_output(output)
