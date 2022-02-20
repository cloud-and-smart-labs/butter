import click
import src.inventory.commands as inventory
import src.ssh.commands as ssh


@click.group()
@click.version_option(version='0.0.2a', message='Butter 🧈 Version: 0.0.2a')
def cli():
    '''
    Butter 🧈 The SSH Client for IoT
    '''


@cli.group('inventory')
def inventory_cmds():
    '''
    Inventory management commands
    '''


@cli.group('exe')
def execute():
    '''
    Command execute (exe: execute)
    '''


@click.command('sh')
@click.argument('inventory-name')
@click.argument('cmd', nargs=-1)
@click.option('-s', 'stream',  flag_value=True, help='Serially Streaming')
def execute_shell(inventory_name: str, cmd: tuple, stream):
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
    if stream:
        ssh.shell_command_stream(inventory_name, cmd)
    else:
        ssh.shell_command(inventory_name, cmd)


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
@click.option('-a', 'all',  flag_value=True, help='Show all including hosts')
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
@click.option('-a', 'all',  flag_value=True, help='Delete all')
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
