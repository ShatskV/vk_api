import os
from urllib.parse import unquote_plus, urlsplit


def make_filepath(url, filepath_template):
    clear_url = unquote_plus(url)
    url_parts = urlsplit(clear_url)
    _, ext = os.path.splitext(url_parts.path)
    if not ext:
        return
    return f'{filepath_template}{ext}'
