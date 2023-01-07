from dotenv import load_dotenv
import rich
import os
import click
import dataset
import streamsb
import streamtape
import guessit
import json
from guessit.jsonutils import GuessitEncoder

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
TABLE_NAME = os.getenv('DATABASE_TABLE')
TABLE_TRUNK = f'wp_trunk_{TABLE_NAME}'
db = dataset.connect(DATABASE_URL)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('wp_id')
@click.argument('filename')
@click.argument('source', type=click.Choice("streamsb,streamtape".split(",")))
@click.argument('content')
def create(wp_id, filename, source, content):
    trunk = db[TABLE_TRUNK]

    guessit_data = guessit.guessit(filename)
    r = trunk.insert(
        dict(wp_id=wp_id,
             filename=filename,
             source=source,
             content=content,
             guessit=json.dumps(guessit_data,
                                cls=GuessitEncoder,
                                ensure_ascii=False)))
    rich.print(r)


@cli.command()
def list():
    trunk = db[TABLE_TRUNK]
    for entry in trunk:
        rich.print(entry)


cli = click.CommandCollection(sources=[cli, streamsb.cli, streamtape.cli])

if __name__ == "__main__":
    cli()
