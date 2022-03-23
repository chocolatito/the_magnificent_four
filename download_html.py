import requests
from pathlib import PurePath

# ___________________________
from open_utils import content_reader, content_writer

# __________________________
# storage html in local disc

def download_pages():
    urls = [url.strip() for url in content_reader('urls.txt', True)]
    file_paths = []

    for url in urls:
        file_path = PurePath(url).name

        try:
            response = requests.get(url)
            if response.ok:
                text = response.text
        except requests.exceptions.ConnectionError as exc:
            print(exc)
            text = ''

        content_writer(f'./html_codes/{file_path}', text)
        file_paths.append(file_path)
    return file_paths
