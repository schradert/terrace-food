###################
### PRELIMINARY ###
###################

# 1. Dates were collected by typing the starting date listed in the header pictures of each menu into JSON
# 2. Some dates were not Mondays (how each weekly menu starts), so the following code was run to change them
def change_dates():
    import json
    import datetime
    with open('menus/dates.json') as f:
        dates = json.load(f)
    for key in dates.keys():
        year, month, day = dates[key].split('-')
        dates[key] = datetime.date(int(year), int(month), int(day))
    for key, date in dates.items():
        if (weekday := date.weekday()) != 0:
            dates[key] = date.replace(day=date.day + 7 - weekday)
    with open('menus/dates.json', 'w') as f:
        json.dump(dates, f, indent=4, default=str)
# 3. The following quick analysis demonstrated repeated dates from different menus:
def repeated_menus():
    import json
    import pandas as pd
    with open('menus/dates.json') as f:
        dates = json.load(f)
    dates_frame = pd.DataFrame(list(dates.items()), columns=['file', 'date'])
    counts = dates_frame['date'].value_counts()
    dup_indices = counts[counts > 1].index
    print(dates_frame[dates_frame['date'].isin(dup_indices)].sort_values('date'))
# 4. Feedback from Steve helped us identify which of each pair was correct.
# 5. The following code was used to filter and modify the dates:
def finalize_dates():
    import json
    with open('menus/dates.json') as f:
        dates = json.load(f)
    dates['Weekly Dinner Menu Week 38.docx'] = '2015-01-19'  # wrong year was listed on menu
    dates.pop('Weekly Dinner Menu Week 54 R26.docx')  # earlier version
    dates.pop('Weekly Dinner Menu Week 56 R26.docx')  # earlier version
    dates.pop('Weekly Dinner Menu Week 57.docx')  # earlier version
    dates.pop('Weekly Dinner Menu Week 57 R42.docx')  # earlier version
    with open('menus/dates.json', 'w') as f:
        json.dump(dates, f, indent=4, default=str)

#############################
### IMPORTS AND CONSTANTS ###
#############################

import json
import re
import datetime
from functools import reduce
from os import listdir
from docx import Document

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
TAG_MATCH = r'\s?\(\s?(V|Veg|GF|D|N|Vegetarian|Vegan|Contains Nuts)\s?\)'
EMDASH = b'\xe2\x80\x93'
EXCEPTIONS = ['No Meal', '---', 'No Diner', 'Winter Break', 'Breakfast Served', 'Lunch Served', 'Service', 'Kitchen Closed', 'Lawn Parties', '2017', 'Formal', '2019', '2018', '2016', '2015', '2014']

####################
### DATA LOADING ###
####################

path = 'menus/main/docx/'
filenames = listdir(path)
docs = [Document(path + name) for name in filenames]
texts = [list(map(lambda p: p.text, doc.paragraphs)) for doc in docs]

with open('menus/dates.json') as f:
    _loaded = json.load(f)
    names, dates = _loaded.keys(), _loaded.values()

#################
### FUNCTIONS ###
#################

def simplify_tags(tags):
    def simplify(tag):
        if tag == 'V':
            return 'Vegan'
        elif tag == 'Veg':
            return 'Vegetarian'
        elif tag == 'GF':
            return 'Gluten-Free'
        elif tag in ('N', 'Contains Nuts'):
            return 'Nuts'
        elif tag == 'D':
            return 'Dairy'
        return tag
    return list(map(simplify, tags))

def count2type(idx):
    if idx == 1:
        return 'soup'
    elif idx in range(2,5):
        return 'entree'
    elif idx in range(5,8):
        return 'side'
    return 'dessert'

def is_valid_dish(line):
    line = line.strip()
    if len(line) == 0:  # empty lines GENERALLY separate days
        return False
    if any([word in line for word in EXCEPTIONS]):
        return False
    return True

def extract_name(line):
    line = line.replace('w.', 'with ')\
               .replace('  ', ' ')\
               .replace('&', 'and')\
               .replace('*', '')
    return re.sub(TAG_MATCH, '', line).strip()

def clean_theme(encoding):
    theme = encoding.split(EMDASH)[-1]\
                    .strip()\
                    .decode('utf-8')\
                    .strip()
    if 'patrick' in theme:
        theme = 'irish'
    elif any([event in theme for event in ['soph', 'lawn', 'formal', 'choice', 'fine']]):
        theme = 'EVENT'
    elif theme == 'vive la france':
        theme = 'french'

    return re.sub(r'night|nite|dinner|!|oktoberfest|day|style|family|', '', theme.lower()).strip()
    

def _builder(args):
    # `name` is currently not used (TODO: incorporate into data by parsing revision state)

    text, name, date_ = args
    date = datetime.datetime.strptime(date_, '%Y-%m-%d').date()

    in_day = False  # keeps track of whether lines represent dishes or random text
    dish_idx = 0  # line number beneath the day of the week subtitle
    data = []  # data object being built!

    # iterate through every line in the document, building `data` in the process
    for line in text:
        if not in_day:
            which_day = list(map(lambda day: line.startswith(day), WEEKDAYS))
            is_new_day = any(which_day)
            if is_new_day:
                in_day = True
                dish_idx = 1
                day = which_day.index(True)
                data.append({  # day structure
                    'weekday':WEEKDAYS[day],
                    'date': date + datetime.timedelta(days=day),
                    'dishes':[]})
                if EMDASH in (encoding := line.encode('utf-8')):
                    data[-1]['theme'] = clean_theme(encoding)
        else:
            is_dish = is_valid_dish(line)
            if not is_dish:
                in_day = False
                continue
            dish_type = count2type(dish_idx)
            dish_idx += 1
            data[-1]['dishes'].append({  # dish structure!
                'type': dish_type,
                'tags': simplify_tags(re.findall(TAG_MATCH, line)),
                'name': extract_name(line)})
            if dish_idx == 9:
                in_day = False

    return data

def data_builder(texts_, names_, dates_):
    built = map(_builder, zip(texts_, names_, dates_))
    return [day for arr in list(built) for day in arr]

#################
### MAIN LOOP ###
#################

data = data_builder(texts, names, dates)
with open('menus/data.json', 'w') as f:
    json.dump(data, f, indent=4, default=str)