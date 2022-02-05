import click
import src.inventory.commands as inventory
from src.inventory.inventory import Inventory
from src.ssh import SSH


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


@cli.group('x')
def execute():
    '''
    Command execute (x: execute)
    '''


def show(output):
    click.secho(
        f" {output.get_ssh_id()} ",
        bold=True,
        bg='cyan',
        nl=False
    )
    click.secho(
        f" STATUS {output.get_status()} ",
        bold=True,
        bg='green',
        fg='white',
        nl=False
    ) if 0 == output.get_status(
    ) else click.secho(
        f" STATUS {output.get_status()} ",
        bold=True,
        bg='red',
        fg='white',
        nl=False
    )
    click.secho(
        f"\t `$ {output.get_command()}` \t",
        bg='white',
        fg='black',
        italic=True
    )

    if 0 == output.get_status():
        click.secho(output.get_output())
    else:
        click.secho(
            output.get_error(),
            fg='red'
        )


@click.command('sh')
@click.argument('inventory-name')
@click.argument('cmd', nargs=-1)
def execute_shell(inventory_name: str, cmd: str):
    '''
    Execute Shell command
    \n
    argument(s):
    \n
    \t 1. Inventory name
    \t 2. Command
    \n
    Example:
    \n
    \t `butter x sh my_inventory_name docker image ls`
    \n
    \t `bx my_inventory_name `ls -la``
    '''
    cmd = ' '.join(cmd)

    for host in Inventory(inventory_name).get_inventory_list():
        ssh_connection = SSH(host[0], host[1], port=int(host[2]))
        output = ssh_connection.command(cmd)
        ssh_connection.close()
        show(output)


@click.command('create')
@click.argument('inventory-names', nargs=-1)
def inventory_create(inventory_names: tuple):
    '''
    Create new inventory
    \n
    argument(s):
    \n
    \t 1. Inventory name
    \n
    Example:
    \n
    \t `$ butter i create inventory_name-1 inventory_name-2`
    \n
    '''
    inventory.create(inventory_names)


@click.command('add')
@click.argument('inventory-name')
@click.argument('ssh-ids', nargs=-1)
@click.option('-p', '--port', default=22, help='PORT number of SSH server')
def inventory_add(inventory_name: str, ssh_ids: tuple, port: int):
    '''
    Add new inventory
    \n
    argument(s):
    \n
    \t 1. Inventory name \n
    \t 2. SSH IDs
    \n
    Example:
    \n
    \t `$ butter i add inventory_name root@localhost root@globallhost`
    '''
    inventory.add(inventory_name, ssh_ids, port)


@click.command('rm')
@click.argument('inventory-name')
@click.argument('ssh-ids', nargs=-1)
def inventory_remove(inventory_name: str, ssh_ids: tuple):
    '''
    Remove host from inventory
    argument(s):
    \n
    \t 1. Inventory name \n
    \t 2. SSH IDs
    \n
    Example:
    \n
    \t `$ butter i remove inventory_name root@localhost root@globalhost`
    '''
    inventory.remove(inventory_name, ssh_ids)


@click.command('ls')
@click.argument('inventory-names', nargs=-1)
@click.option('-a', 'all',  flag_value=True)
def inventory_show(inventory_names: str, all):
    '''
    List of the inventory
    argument(s):
    \n
    \t 1. Inventory name \n
    \n
    switch(s):
    \n
    \t -a : All \n
    \n
    Example:
    \n
    \t `$ butter i ls inventory_name_1 inventory_name_2` \n
    \t `$ butter i ls -a` \n
    \n
    '''
    if all:
        inventory.inventory_list(True)
    else:
        if inventory_names:
            inventory.host_list(inventory_names)
        else:
            inventory.inventory_list()


@click.command('clear')
@click.argument('inventory-names', nargs=-1)
@click.option('-a', 'all',  flag_value=True)
def inventory_clear(inventory_names: tuple, all):
    '''
    Delete inventory
    argument(s):
    \n
    \t 1. Inventory name \n
    \n
    switch(s):
    \n
    \t -a : All \n
    \n
    Example:
    \n
    \t `$ butter i clear inventory_name_1 inventory_name_3` \n
    \t `$ butter i clear -a` \n
    \n
    '''
    if all:
        inventory.clear_all()
    else:
        if inventory_names:
            inventory.clear(inventory_names)


inventory_cmds.add_command(inventory_create)
inventory_cmds.add_command(inventory_add)
inventory_cmds.add_command(inventory_remove)
inventory_cmds.add_command(inventory_show)
inventory_cmds.add_command(inventory_clear)
execute.add_command(execute_shell)
