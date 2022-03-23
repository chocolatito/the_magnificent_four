import csv
from os import listdir
from distutils.sysconfig import PREFIX
from bs4 import BeautifulSoup
# ___________________________________________________
from open_utils import content_reader, content_writer
from download_html import download_pages
# _______________________________________________________________
WIKITABLE_COLLAPSIBLE_CLASS = 'wikitable collapsible uncollapsed'
IMG_URL_PREFIX = '//upload.wikimedia.org/wikipedia/commons/'


#
#
# __________________
def parse_html(path):
    content = content_reader(f'./html_codes/{path}')
    return BeautifulSoup(content, 'html.parser')
# ______________________________________________


# ________________________________________________________
def write_html_tables(path, subfix, is_collapsible=False):
    soup = parse_html(path)
    if is_collapsible:
        table = soup.find('table', {'class': f'{WIKITABLE_COLLAPSIBLE_CLASS}'})
    else:
        table = soup.find(lambda tag: tag.name ==
                          'table' and tag.get('class') == ['wikitable'])
    content_writer(f'./html_codes/{path}{subfix}', f'{table}')
# ________________________________________________


# ___________________________
def get_src_of_value(td_tag):
    srcset_list = td_tag.a.img['srcset'].split(' ')
    return [s for s in srcset_list if s.startswith(IMG_URL_PREFIX)].pop()


def get_list_tuples(path):
    soup = parse_html(path)
    url_img = get_src_of_value(soup.find('td', {'class': 'infobox-image'}))
    # a tuple with key and value in string >> "('key', 'value'),"
    return f"('{path}','https:{url_img}'),"
# _____________________________________________________


# __________________________________________________
def get_table_paths(file_paths, subfix='wikitable'):
    return [f'{path}_{subfix}' for path in file_paths]


def get_paths_for_csv(file_paths, subfix='_wikitable'):
    return [f'./csv_files/{path}{subfix}' for path in file_paths]
# _______________________________________________________________


# _________________________
def format_text_item(item):
    item.replace(';', '.')
    item.replace('\n', '')
    return item.replace('\t', '').strip()


def get_rows(path):
    table = content_reader(f'./html_codes/{path}')
    soup = BeautifulSoup(table, 'html.parser')
    rows = []
    for tr_list in soup.select('tbody tr'):
        rows.append([format_text_item(tr.text)
                    for tr in tr_list if tr != '\n'])
    return rows


def write_csvs(file_paths, table_for_csv):
    for i in range(len(file_paths)):
        path = f'{file_paths[i]}.csv'
        with open(path, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            [writer.writerow(row) for row in table_for_csv[i]]
# _________________________________________________________________________________


# ________________________________________________________________________________
# Future main script

# Download pages and generate <file_paths> ______________________________________
# return path for find html files in ./html_codes/ dir
file_paths = download_pages()

# Generate files with wikipedia table __________________________________________
for path in file_paths:
    write_html_tables(path, '_wikitable_collapsible', True)
    write_html_tables(path, '_wikitable')

# Get image ___________________________________________________________________
string_of_tuples = "".join([get_list_tuples(path) for path in file_paths])
content_writer(f'img_urls.txt', string_of_tuples, 'w')

# Writing .csv files __________________________________________________________
# _wikitable paths
wk_t_paths = get_table_paths(file_paths)

# _wikitable_collapsible paths
wk_cllps_t_paths = get_table_paths(file_paths, 'wikitable_collapsible')

#
#
wk_t_row_list = [get_rows(path) for path in wk_t_paths]
paths_for_csv = get_paths_for_csv(file_paths)
write_csvs(paths_for_csv, wk_t_row_list)
#
wk_cllps_t_row_list = [get_rows(path) for path in wk_cllps_t_paths]
paths_for_csv = get_paths_for_csv(file_paths, '_wikitable_collapsible')
write_csvs(paths_for_csv, wk_cllps_t_row_list)
