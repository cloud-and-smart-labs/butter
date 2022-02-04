import click
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
    click.secho(f" {output.get_ssh_id()} ", bold=True, bg='cyan', nl=False)
    click.secho(f" STATUS {output.get_status()} ", bold=True, bg='green', fg='white', nl=False) if 0 == output.get_status(
    ) else click.secho(f" STATUS {output.get_status()} ", bold=True, bg='red', fg='white', nl=False)
    click.secho(f"\t `$ {output.get_command()}` \t",
                bg='white', fg='black', italic=True)

    if 0 == output.get_status():
        click.secho(output.get_output())
    else:
        click.secho(output.get_error(), fg='red')


@click.command('sh')
@click.argument('inventory-name')
@click.argument('cmd')
def execute_shell(inventory_name: str, cmd: str):
    '''
    Execute Shell command
    '''
    for host in Inventory(inventory_name).get_inventory_list():
        ssh_connection = SSH(host[0], host[1], port=int(host[2]))
        output = ssh_connection.command(cmd)
        ssh_connection.close()
        show(output)


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
    click.secho('HOSTNAME\tUSERNAME\tPORT', bold=True, fg='green')
    if hosts:
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
execute.add_command(execute_shell)
