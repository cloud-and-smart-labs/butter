import click
from src.inventory.inventory import Inventory


@click.group()
def cli():
    '''
    Butter : The SSH Client for IoT
    '''


@cli.group('i')
def inventory_cmds():
    '''
    Inventory management commands (i: inventory)
    '''


@click.command('create')
@click.argument('name')
def inventory_create(name: str):
    '''
    Create new inventory
    \n
    argument(s):
    \n
    \t 1. Inventory name
    \n
    Example:
    \n
    \t `$ butter inventory create my_inventory_name`
    '''
    Inventory(name).create()


@click.command('add')
@click.argument('inventory-name')
@click.argument('ssh-id')
@click.option('-p', '--port', default=22, help='PORT number of SSH server')
def inventory_add(inventory_name: str, ssh_id: str, port):
    '''
    Add new inventory
    \n
    argument(s):
    \n
    \t 1. Inventory name \n
    \t 2. SSH ID
    \n
    Example:
    \n
    \t $ butter inventory add my_inventory_name root@localhost
    '''
    if '@' in ssh_id:
        username, hostname = ssh_id.split('@')
        Inventory(inventory_name).add_host(hostname, username, port)
    else:
        click.echo(ssh_id, nl=False)
        click.secho('\tNot A SSH ID', fg='red', bold=True)


@click.command('rm')
@click.argument('inventory-name')
@click.argument('ssh-id')
def inventory_remove(inventory_name: str, ssh_id: str):
    '''
    Remove host from inventory
    argument(s):
    \n
    \t 1. Inventory name \n
    \t 2. SSH ID
    \n
    Example:
    \n
    \t $ butter inventory remove my_inventory_name root@localhost
    '''
    if '@' in ssh_id:
        _, ssh_id = ssh_id.split('@')
    Inventory(inventory_name).remove_host(ssh_id)


@click.command('ls')
@click.argument('inventory-name')
def inventory_show(inventory_name: str):
    '''
    List of the inventory
    argument(s):
    \n
    \t 1. Inventory name \n
    \n
    Example:
    \n
    \t $ butter inventory ls my_inventory_name
    '''
    hosts = Inventory(inventory_name).get_inventory_dict()
    if hosts:
        click.secho('HOSTNAME\tUSERNAME\tPORT', bold=True, fg='green')
        for host in hosts:
            click.echo(
                f"{host['hostname']}\t{host['username']}\t\t{host['port']}")


@click.command('clear')
@click.argument('inventory-name')
def inventory_clear(inventory_name: str):
    '''
    Delete inventory
    argument(s):
    \n
    \t 1. Inventory name \n
    \n
    Example:
    \n
    \t $ butter inventory clear my_inventory_name
    '''
    Inventory(inventory_name).clear()


inventory_cmds.add_command(inventory_create)
inventory_cmds.add_command(inventory_add)
inventory_cmds.add_command(inventory_remove)
inventory_cmds.add_command(inventory_show)
inventory_cmds.add_command(inventory_clear)
