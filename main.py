from dotenv import load_dotenv
import rich
import os
import click
import dataset

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
TABLE_TRUNK = 'wp_lazy_trunk'
db = dataset.connect(DATABASE_URL)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('wp_id')
@click.argument('content')
def create(wp_id, content):
    trunk = db[TABLE_TRUNK]
    r = trunk.insert(dict(wp_id=wp_id, content=content))
    rich.print(r)


@cli.command()
def list():
    trunk = db[TABLE_TRUNK]
    for entry in trunk:
        rich.print(entry)


if __name__ == "__main__":
    cli()
