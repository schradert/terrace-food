import dash
import flask
import os
from dash.dependencies import Input, Output, State
import dash_core_components as dcc 
import dash_html_components as html
from pymongo import MongoClient

PRIMARY_TABS = ('missing', 'dishes', 'themes', 'adjs', 'nouns',
                'noun_phrases_1+', 'noun_phrases_2+')
SECONDARY_TABS = ('soup', 'entree', 'side', 'dessert')
PRIMARY_TABS_NAMES = ('Missing', 'Dishes', 'Themes', 'Adjectives', 'Nouns',
                      'Noun Phrases (ALL)', 'Noun Phrases (COMPOSITE)')

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                meta_tags=[{"name": "viewport",
                            "content": "width=device-width, initial-scale=1"}])
client = MongoClient(os.environ.get('CLIENT_URI'))
coll = client.terrace_food.graphs

def get_graph(tab1, tab2):
    if tab1 == 'missing':
        graph = coll.find_one({})
    elif tab1 == 'themes':
        graph = coll.find_one({'layout.title.text':tab1})
    else:
        graph = coll.find_one({'layout.title.text':f'{tab1}_{tab2}'})
    graph.pop('_id')
    return graph

def _display(tab1, tab2):
    graph = get_graph(tab1, tab2)
    return dcc.Graph(figure=graph)

app.layout = html.Div([
    dcc.Tabs(
        id='primary-tabs',
        value='dishes',
        children=[
            dcc.Tab(
                value=tab,
                label=PRIMARY_TABS_NAMES[PRIMARY_TABS.index(tab)]
            ) for tab in PRIMARY_TABS]),
    dcc.Tabs(
        id='secondary-tabs',
        value='entree',
        children=[
            dcc.Tab(
                value=tab_,
                label=f'{tab_.capitalize()}s'
            ) for tab_ in SECONDARY_TABS]),
    html.Div(
        id='graph-container',
        children=_display('dishes', 'entree')) 
])



@app.callback(
    output=Output('graph-container', 'children'),
    inputs=[Input('primary-tabs', 'value'),
            Input('secondary-tabs', 'value')])
def switch_secondary(tab1, tab2):
    return _display(tab1, tab2)

@app.callback(
    output=Output('secondary-tabs', 'style'),
    inputs=[Input('primary-tabs', 'value')])
def switch_primary(tab1):
    hide_secondary = tab1 in ('missing', 'themes')
    return {'display':'none' if hide_secondary else 'block'}

if __name__ == '__main__':
    app.run_server(debug=True)