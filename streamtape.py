import click
import requests
import os
import hashlib
import rich

STREAMTAPE_LOGIN = os.getenv('STREAMTAPE_LOGIN')
STREAMTAPE_KEY = os.getenv('STREAMTAPE_KEY')


@click.group()
def cli():
    pass


@cli.command('upload_streamtape')
@click.argument('file', type=click.Path(exists=True))
def upload(file):
    sha256hash = ''
    with open(file, 'rb') as f:
        sha256hash = hashlib.sha256(f.read()).hexdigest()

    params = {
        'key': STREAMTAPE_KEY,
        'login': STREAMTAPE_LOGIN,
        'sha256': sha256hash,
    }

    rich.print('[white on yellow]generating upload url')
    response = requests.get("https://api.streamtape.com/file/ul",
                            params=params)
    response.raise_for_status()
    url_upload = response.json().get("result", {}).get('url')
    files = {'file': open(file, 'rb')}
    rich.print('[white on yellow]uploading ...')
    resp = requests.post(url_upload, files=files)
    resp.raise_for_status()
    upload_data = resp.json()
    rich.print(upload_data)
    url = upload_data.get('result', {}).get('url')
    new_url = url.replace('.com/v/', '.com/e/')
    rich.print(new_url, end='')
    return new_url


if __name__ == "__main__":
    cli()
