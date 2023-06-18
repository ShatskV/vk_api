import os
from pathlib import Path
from urllib.parse import unquote_plus, urlsplit

import requests

# from settings import logger


def rm_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)


def make_filepath(url, filepath_template):
    clear_url = unquote_plus(url)
    url_parts = urlsplit(clear_url)
    _, ext = os.path.splitext(url_parts.path)
    if not ext:
        return
    return f'{filepath_template}{ext}'
        

def get_and_save_image_to_disk(image_url, filepath_template, params=None):
    directory = Path(filepath_template).parent
    Path(directory).mkdir(parents=True, exist_ok=True)
    response = requests.get(image_url, params=params)
    response.raise_for_status()
    image = response.content
    filepath = make_filepath(image_url, filepath_template)    
    if not filepath:
        # logger.error(f'url: {image_url} This is not image url')
        print(f'url: {image_url} This is not image url')
        return
    with open(filepath, 'wb') as file:
        file.write(image)
