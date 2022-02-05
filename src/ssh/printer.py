from click import echo, secho


def command_output(output):
    'Show command output from `Output` object'

    # SSH ID
    secho(
        f" {output.get_ssh_id()} ",
        bold=True,
        bg='cyan',
        nl=False
    )

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

    # Shell command
    secho(
        f"\t `$ {output.get_command()}` \t",
        bg='white',
        fg='black',
        italic=True
    )

    # Command output
    if 0 == output.get_status():
        echo(output.get_output())

    # Command error
    else:
        secho(
            output.get_error(),
            fg='red'
        )
