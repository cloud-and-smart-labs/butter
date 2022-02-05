from src.inventory.printer import *
from src.inventory.inventory import Inventory


# Create commands
def create(inventory_names: tuple) -> None:
    'Create inventory'
    heading('Inventory Create')
    for inventory in inventory_names:
        Inventory(inventory).create()
        list_item(inventory)


def add(inventory_name: str, ssh_ids: tuple, port=22) -> None:
    'Add host into inventory'
    heading(f'Inventory Add : {inventory_name}')
    for ssh_id in ssh_ids:
        if '@' in ssh_id:
            username, hostname = ssh_id.split('@')
            Inventory(inventory_name).add_host(hostname, username, port)
            list_item(ssh_id)
        else:
            error(f'{ssh_id} NOT A SSH ID')


# Remove commands
def remove(inventory_name: str, ssh_ids: tuple) -> None:
    'Remove host from inventory'
    heading(f'Remove Host(s) : {inventory_name}')
    for ssh_id in ssh_ids:
        if '@' in ssh_id:
            _, hostname = ssh_id.split('@')
            Inventory(inventory_name).remove_host(hostname)
            list_item(ssh_id)
        else:
            error(f'{ssh_id} NOT A SSH ID')


# List commands
def inventory_list(all=False) -> None:
    'List out inventories'
    heading('Inventories')
    for inventory in Inventory().get_all_inventory():
        if all:
            # List all host as well
            host_list((inventory,))
        else:
            list_item(inventory)


def host_list(inventory_names: tuple) -> None:
    'List out hosts from inventory'
    for inventory in inventory_names:
        heading(inventory)
        hosts = Inventory(inventory).get_inventory_dict()
        tabular_heading(
            'HOSTNAME',
            'USERNAME',
            'PORT'
        )
        for host in hosts:
            tabular_item(
                host['hostname'],
                host['username'],
                f"\t {host['port']}",
            )


# Delete commands
def clear(inventory_names: tuple) -> None:
    'Delete inventory'
    heading('Inventory Clear')
    for inventory in inventory_names:
        Inventory(inventory).clear()
        list_item(inventory)


def clear_all() -> None:
    'Delete all inventories'
    clear(Inventory().get_all_inventory())
