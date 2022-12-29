import click
from dotenv import load_dotenv
import rich
import requests
import os

load_dotenv()

SERVER_URL = 'https://api.streamsb.com/api/upload/server'
API_KEY = os.getenv("STREAMB_API_KEY")
end_url = 'https://sbchill.com/c/{code}.html'


@click.group()
def cli():
    pass


@cli.command('upload_streamsb')
@click.argument('file', type=click.Path(exists=True))
def upload(file):
    params = {
        'key': API_KEY,
    }
    rich.print('[white on blue]generating upload url')
    response = requests.get(SERVER_URL, params=params)
    response.raise_for_status()
    url_upload = response.json().get('result')
    data = {
        'api_key': API_KEY,
        'json': 1,
    }
    files = {'file': open(file, 'rb')}
    rich.print('[white on blue]uploading ...')
    resp = requests.post(url_upload, files=files, data=data)
    resp.raise_for_status()
    upload_data = resp.json()
    rich.print(upload_data)
    status = upload_data.get('result')[0].get('status')
    assert status == "OK", ':('
    code = upload_data.get('result', [{}])[0].get("code")
    rich.print(end_url.format(code=code), end='')


if __name__ == "__main__":
    upload()
