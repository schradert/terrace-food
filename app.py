import dash
import flask
import os
import dash_core_components as dcc 
import dash_html_components as html
from pymongo import MongoClient

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

client = MongoClient('mongodb://localhost:27017')

def get_graphs():
    graphs = [graph for graph in client.terrace_food.graphs.find()]
    print(type(graphs))
    for graph in graphs:
        graph.pop('_id')
    return graphs

app.layout = html.Div([
    dcc.Graph(figure=graph)\
    for graph in get_graphs()
])

if __name__ == '__main__':
    app.run_server(debug=True)