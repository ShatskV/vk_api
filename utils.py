import os
from pathlib import Path
from urllib.parse import unquote_plus, urlsplit

import requests


def make_filepath(url, filepath_template):
    clear_url = unquote_plus(url)
    url_parts = urlsplit(clear_url)
    _, ext = os.path.splitext(url_parts.path)
    if not ext:
        return
    return f'{filepath_template}{ext}'
        

def get_image_from_url(image_url, params=None):
    response = requests.get(image_url, params=params)
    response.raise_for_status()
    image = response.content
    return image


def save_image_to_disk(image, filepath):
    directory = Path(filepath).parent
    Path(directory).mkdir(parents=True, exist_ok=True)
    with open(filepath, 'wb') as file:
        file.write(image)
