import ast
import csv
import re
import datetime as dt
from dateutil.relativedelta import relativedelta
# ___________________________________
from open_utils import content_reader


# ______________________________
def get_percent(partial, total):
    return "{0:.2f}".format(100 * int(partial) / int(total))


# ___________________________
def get_fight_date(fight_at):
    date = fight_at.replace(' ', '')
    try:
        return dt.datetime.strptime(date, f'%b%d,%Y')
    except (ValueError, TypeError):
        return dt.datetime.strptime(date, f'%B%d,%Y')


def get_years_and_days(born_at, fight_at):
    born = dt.datetime.strptime(born_at, '%b %d, %Y')
    fight_date = get_fight_date(fight_at)

    age = relativedelta(fight_date, born)
    birth_date = born+relativedelta(years=age.years)
    return f"{age.years} years, {(fight_date-birth_date).days} days"
# ___________________________________________________________________


# ______________________
def get_rows(core_path):
    with open(f'csv_files/{core_path}.csv', 'r') as fh:
        rows = [row for row in csv.reader(fh)]
    return rows


# _____________________________
def get_sumary_dict(core_path):
    with open(f'csv_files/{core_path}.csv', 'r') as fh:
        rows = [row for row in csv.reader(fh)]
    sumary_dict = {
        'total_fights': re.sub('[a-z]|\xa0| ', '', rows[0][0]),
        'total_wins': re.sub('[a-z]|\xa0| ', '', rows[0][1]),
        'total_losses': re.sub('[a-z]|\xa0| ', '', rows[0][2]),
        'wins_ko': rows[1][1],
        'losses_ko': rows[1][2],
        'wins_decision': rows[2][1],
        'losses_decision': rows[2][2]
    }
    ALTERNATIVES_RESULTS = ['wins_disqualification',
                            'losses_disqualification',
                            'nocontests',
                            'draws',
                            ]
    for row in rows[3:]:
        if re.sub(' |\xa0', '', row[0]).lower() == 'bydisqualification':
            sumary_dict['wins_disqualification'] = row[1]
            sumary_dict['losses_disqualification'] = row[2]
        elif re.sub(' |\xa0', '', row[0]).lower() == 'nocontests':
            sumary_dict['nocontests'] = row[1]
        else:
            sumary_dict['draws'] = row[1]

    # The table may not contain any alt. results.
    for result in ALTERNATIVES_RESULTS:
        if not (result in sumary_dict):
            sumary_dict[result] = '0'
    return sumary_dict


def generate_md(core_path, born_at, src_image):
    sumary_dict = get_sumary_dict(f'{core_path}_wikitable_collapsible')
    rows = get_rows(f'{core_path}_wikitable')
    #
    rows[0].insert(7, 'Age')
    thead = f"|{'| '.join([item for item in rows[0]])}|"
    tbody_list = []
    for x in range(1, len(rows), 1):
        fight_at = rows[x][6]
        rows[x].insert(7, get_years_and_days(born_at, fight_at))
        tbody_list.append(f"|{'|'.join([item for item in rows[x]])}|")

    BLANKSPACE = ' '
    UNDERSCORE = '_'

    subtitle = '\n\n---\n## Professional boxing record\n'
    separator = f"|{'|'.join(['---' for x in range(len(rows[0]))])}|"
    # Statistics
    percent_of_wins = get_percent(
        sumary_dict['total_wins'], sumary_dict['total_fights'])
    percent_of_wins_ko = get_percent(
        sumary_dict['wins_ko'], sumary_dict['total_fights'])
    percent_of_losess = get_percent(
        sumary_dict['total_losses'], sumary_dict['total_fights'])
    percent_of_losess_ko = get_percent(
        sumary_dict['losses_ko'], sumary_dict['total_fights'])
    percent_of_draws = get_percent(
        sumary_dict['draws'], sumary_dict['total_fights'])
    image = f"""
---
<p align="center"><img src="{src_image}"></p>
"""

    sumary = f"""
---
### Sumary
___{sumary_dict['total_fights']}_ fights as a professional__
- __{sumary_dict['total_wins']}__ wins:
  + __{sumary_dict['wins_ko']}__ for K.O.
  + __{sumary_dict['wins_decision']}__ for desition.
  + __{sumary_dict['wins_disqualification']}__ for disqualification.
- __{sumary_dict['total_losses']}__ losses:
  + __{sumary_dict['losses_ko']}__ for K.O.
  + __{sumary_dict['losses_decision']}__ for desition.
  + __{sumary_dict['losses_disqualification']}__ for disqualification.
- __{sumary_dict['draws']}__ draws:

---
### Statistics
- __{percent_of_wins}__ % Winning
  + {percent_of_wins_ko}__ % Winning
- __{percent_of_losess}__ % Losing
  + __{percent_of_losess_ko}__ % Losing
- __{percent_of_draws}__ % Drawing
"""

    with open(f'./markdown_files/{core_path}.md', 'w') as fh:
        fh.write(f'# {core_path.replace(UNDERSCORE,BLANKSPACE)}')
        fh.write(image)
        fh.write(f'{subtitle}')
        fh.write(f'{sumary}\n')
        fh.write(f'---\n### All career\n')
        fh.write(f'{thead}\n')
        fh.write(f'{separator}\n')
        [fh.write(f'{row}\n') for row in tbody_list]
# __________________________________________________


# ________________________________________________________________________
borns = {
    'Roberto_Dur%C3%A1n':'Jun 16, 1951',
    'Sugar_Ray_Leonard': 'May 17, 1956',
    'Marvelous_Marvin_Hagler': 'May 23, 1954',
    'Thomas_Hearns': 'Oct 18, 1958'
}

src_dict = dict(list(ast.literal_eval(content_reader(f'img_urls.txt'))))
for core_path, born_at in borns.items():
    generate_md(core_path, born_at, src_dict[core_path])
