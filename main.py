from dotenv import load_dotenv
import rich
import os
import click
import dataset
import streamsb

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
TABLE_TRUNK = 'wp_lazy_trunk'
db = dataset.connect(DATABASE_URL)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('wp_id')
@click.argument('filename')
@click.argument('source', type=click.Choice("streamsb,".split(", ")))
@click.argument('content')
def create(wp_id, filename, source, content):
    trunk = db[TABLE_TRUNK]
    r = trunk.insert(
        dict(wp_id=wp_id, filename=filename, source=source, content=content))
    rich.print(r)


@cli.command()
def list():
    trunk = db[TABLE_TRUNK]
    for entry in trunk:
        rich.print(entry)


cli = click.CommandCollection(sources=[cli, streamsb.cli])

if __name__ == "__main__":
    cli()
