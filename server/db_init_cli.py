import click
from database.local_database import DatabaseEditor


@click.command()
@click.option("--force", default=False)
def db_init(force):
    response = DatabaseEditor._init(force=force)  # pylint: disable=protected-access
    click.echo(click.style(text=response))


if __name__ == "__main__":
    db_init()  # pylint: disable=no-value-for-parameter
