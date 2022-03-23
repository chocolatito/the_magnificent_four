import csv
import re
import datetime as dt
from dateutil.relativedelta import relativedelta


def get_fight_date(fight_at):
    date = fight_at.replace(' ', '')
    print(f'fight_at: {fight_at}')
    try:
        return dt.datetime.strptime(date, f'%b%d,%Y')
    except (ValueError, TypeError):
        print(f'date: {date}')
        return dt.datetime.strptime(date, f'%B%d,%Y')


def get_years_and_days(born_at, fight_at):
    born = dt.datetime.strptime(born_at, '%b %d, %Y')
    fight_date = get_fight_date(fight_at)

    age = relativedelta(fight_date, born)
    birth_date = born+relativedelta(years=age.years)
    return f"{age.years} years, {(fight_date-birth_date).days} days"


def get_rows(core_path):
    with open(f'csv_files/{core_path}.csv', 'r') as fh:
        rows = [row for row in csv.reader(fh)]
    return rows


def generate_md(core_path, born_at):
    rows = get_rows(core_path)
    rows[0].insert(7, 'Age')
    thead = f"|{'| '.join([item for item in rows[0]])}|"
    tbody_list = []
    for x in range(1, len(rows), 1):
        fight_at = rows[x][6]
        rows[x].insert(7, get_years_and_days(born_at, fight_at))
        tbody_list.append(f"|{'|'.join([item for item in rows[x]])}|")

    blankspace = ' '
    underscore = '_'
    subtitle = '\n\n---\n## Professional boxing record\n'
    separator = f"|{'|'.join(['---' for x in range(len(rows[0]))])}|"

    with open(f'./markdown_files/{core_path}.md', 'w') as fh:
        fh.write(f'# {core_path.replace(underscore,blankspace)}{subtitle}')
        fh.write(f'{thead}\n')
        fh.write(f'{separator}\n')
        [fh.write(f'{row}\n') for row in tbody_list]


# ________________________________________________________________________
borns = {
    'Sugar_Ray_Leonard': 'May 17, 1956',
    'Marvelous_Marvin_Hagler': 'May 23, 1954',
    'Thomas_Hearns': 'Oct 18, 1958'
}
[generate_md(core_path, born_at) for core_path, born_at in borns.items()]
