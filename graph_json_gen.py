import plotly.graph_objs as go
import plotly.express as px 
import pandas as pd
import nbformat 
import json
import datetime
from pymongo import MongoClient



with open('menus/data.json') as f:
    data = sorted(json.load(f), key=lambda day: day['date'])

# MISSING DATA GRAPH
existing_dates = [datetime.datetime.strptime(day['date'], '%Y-%m-%d').date()\
                  for day in data if len(day['dishes']) > 0]
first_day, last_day = existing_dates[0], existing_dates[-1]
all_dates = [first_day + datetime.timedelta(days=i)\
             for i in range(abs((last_day - first_day).days) + 1)]
missing_dates = [date for date in all_dates if date not in existing_dates]
dates_chunked = [[existing_dates[0]]]
for date in existing_dates[1:]:
    if date == dates_chunked[-1][-1] + datetime.timedelta(days=1):
        dates_chunked[-1].append(date)
    else:
        dates_chunked.append([date])
missing_dates_chunked = [[missing_dates[0]]]
for date in missing_dates[1:]:
    if date == missing_dates_chunked[-1][-1] + datetime.timedelta(days=1):
        missing_dates_chunked[-1].append(date)
    else:
        missing_dates_chunked.append([date])

missing_df = pd.DataFrame([
    {'Task':f'Week {i+1}', 
     'Start':str(chunk[0]), 
     'Finish':str(chunk[-1]), 
     'Resource':status}\
    for status, dataset in zip(
        ('existing', 'missing'), 
        (dates_chunked, missing_dates_chunked)) \
    for i, chunk in enumerate(dataset)])
missing_fig = px.timeline(missing_df, x_start="Start", x_end="Finish", y="Resource", color="Resource")

# COMMON DATA GRAPHS
with open('menus/graph_data.json') as f:
    graph_data = json.load(f)

def common_graph_gen(freqs, label):
    x, y = list(zip(*freqs))
    return go.Figure(
        data=[go.Bar(
            x=x, y=y
        )],
        layout={
            'title_text':label
        }
    )

figs = [missing_fig]
for group, freqs in graph_data.items():
    if group != 'themes':
        for type_, items in freqs.items():
            figs.append(common_graph_gen(items[:15], '_'.join((group, type_))))
    else:
        figs.append(common_graph_gen(freqs, group))


client = MongoClient('mongodb://localhost:27017')
db = client.terrace_food
graphs = db.graphs 
graphs.delete_many({})
graphs.insert_many([json.loads(fig.to_json()) for fig in figs])