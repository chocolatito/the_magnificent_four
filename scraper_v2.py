import csv

from bs4 import BeautifulSoup
# ___________________________
from open_utils import content_reader, content_writer
from download_html import download_pages
# ___________________________________________________


def parse_html(path):
    content = content_reader(path)
    return BeautifulSoup(content, 'html.parser')


def write_wikitable(path):
    print
    soup = parse_html(path)
    wikitable = soup.find(lambda tag: tag.name ==
                          'table' and tag.get('class') == ['wikitable'])
    content_writer(f'{path}_wikitable', f'{wikitable}')


# roturn path for find html files in ./html_codes/ dir
file_paths = download_pages()
# Generate files with wikipedia table
[write_wikitable(f'./html_codes/{path.strip()}') for path in file_paths]
# _________________________________________________________


def format_text_item(item):
    item.replace(';', '.')
    item.replace('\n', '')
    return item.replace('\t', '').strip()


def get_rows(wikitable_path):
    wikitable = content_reader(wikitable_path)
    soup = BeautifulSoup(wikitable, 'html.parser')
    rows = []
    for tr_list in soup.select('tbody tr'):
        rows.append([format_text_item(tr.text)
                    for tr in tr_list if tr != '\n'])
    return rows


# __________________________________________________________
wikitable_paths = [f'./html_codes/{path}_wikitable' for path in file_paths]
table_for_csv = [get_rows(path) for path in wikitable_paths]


for i in range(len(file_paths)):
    path = f'csv_files/{file_paths[i]}.csv'
    print(f'Written to:::{path}')
    with open(path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        [writer.writerow(row) for row in table_for_csv[i]]

# _________________________________________________________
