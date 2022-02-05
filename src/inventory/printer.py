from click import secho, echo


def heading(text: str) -> None:
    'Show heading text'
    secho(
        f'  {text}  ',
        bold=True,
        bg='cyan',
        fg='white'
    )


def tabular_heading(*text: str) -> None:
    'Show table heading'
    for word in text:
        echo(' ', nl=False)
        secho(
            f'{word}\t',
            bold=True,
            fg='green',
            nl=False
        )
    echo()


def list_item(text: str) -> None:
    'Show list item'
    echo(f' |- {text}')


def tabular_item(*text: str) -> None:
    'Show table row'
    for word in text:
        echo(' ', nl=False)
        echo(
            f'{word}\t',
            nl=False
        )
    echo()


def error(text: str) -> None:
    'Show error message'
    secho(
        ' ERROR ',
        bold=True,
        bg='red',
        fg='white',
        nl=False
    )
    echo(f' {text}')
