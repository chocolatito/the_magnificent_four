# import ast
# dict(list(ast.literal_eval(text)))
import csv
from distutils.sysconfig import PREFIX

from bs4 import BeautifulSoup
# ___________________________
from open_utils import content_reader, content_writer
from download_html import download_pages
# ___________________________________________________

WIKITABLE_COLLAPSIBLE_CLASS = 'wikitable collapsible uncollapsed'
IMG_URL_PREFIX = '//upload.wikimedia.org/wikipedia/commons/'
HTML_DIR = './html_codes/'
#
# __________________


def parse_html(core_name, subfix=''):
    content = content_reader(HTML_DIR+core_name+subfix)
    return BeautifulSoup(content, 'html.parser')


def write_wikitable(path):
    soup = parse_html(path)
    wikitable = soup.find(lambda tag: tag.name ==
                          'table' and tag.get('class') == ['wikitable'])
    content_writer(f'{path}_wikitable', f'{wikitable}')


def write_wikitable_collapsible(path):
    soup = parse_html(path)
    wikitable_collapsible = soup.find(
        'table', {'class': f'{WIKITABLE_COLLAPSIBLE_CLASS}'})
    content_writer(f'{path}_wikitable_collapsible', f'{wikitable_collapsible}')


#
# _______________________

def write_img_urls(path):
    soup = parse_html(f'./html_codes/{path}')
    srcset_list = soup.find(
        'td', {'class': 'infobox-image'}).a.img['srcset'].split(' ')
    url_img = [s for s in srcset_list if s.startswith(IMG_URL_PREFIX)].pop()
    tup = f"('{path}','https:{url_img}'),"
    content_writer(f'img_urls.txt', tup, 'a')


# roturn path for find html files in ./html_codes/ dir
file_paths = download_pages()
# Generate files with wikipedia table
[write_wikitable(f'./html_codes/{path.strip()}') for path in file_paths]
[write_wikitable_collapsible(
    f'./html_codes/{path.strip()}') for path in file_paths]
# Get image
[write_img_urls(path.strip()) for path in file_paths]
# _________________________________________________________


def format_text_item(item):
    item.replace(';', '.')
    item.replace('\n', '')
    return item.replace('\t', '').strip()


def get_rows(path):
    table = content_reader(path)
    soup = BeautifulSoup(table, 'html.parser')
    rows = []
    for tr_list in soup.select('tbody tr'):
        rows.append([format_text_item(tr.text)
                    for tr in tr_list if tr != '\n'])
    return rows


# __________________________________________________________

def write_csvs(file_paths, table_for_csv):
    print(file_paths)
    for i in range(len(file_paths)):
        path = f'{file_paths[i]}.csv'
        print(f'Written to:::{path}')
        with open(path, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            [writer.writerow(row) for row in table_for_csv[i]]

# _________________________________________________________


wikitable_paths = [f'./html_codes/{path}_wikitable' for path in file_paths]
table_for_csv = [get_rows(path) for path in wikitable_paths]
paths_for_csv = [f'./csv_files/{path}_wikitable' for path in file_paths]

write_csvs(paths_for_csv, table_for_csv)

wikitable_collapsible_paths = [
    f'./html_codes/{path}_wikitable_collapsible' for path in file_paths]
table_for_csv = [get_rows(path) for path in wikitable_collapsible_paths]
paths_for_csv = [
    f'./csv_files/{path}_wikitable_collapsible' for path in file_paths]

write_csvs(paths_for_csv, table_for_csv)
