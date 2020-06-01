# from flask import Blueprint, render_template
#
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
#
# dash_bp = Blueprint('dash_bp', __name__)
#
#
# @dash_bp.route('/')
# def home():
#
#     return render_template('dashhome.html',title='Plotly Flask Tutorial.',template='home-template',body='This is an example homepage served with Flask.')


from dash import Dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import os
import firebase_admin
from firebase_admin import db
import pandas as pd
from pandas.io.json import json_normalize
import json
import csv


def Add_Dash(server):
    # Create Dash app.
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/static/dist/css/styles.css', 'https://fonts.googleapis.com/css?family=Lato',
                            'https://use.fontawesome.com/releases/v5.8.1/css/all.css']
    external_scripts = ['/static/dist/js/includes/jquery.min.js',
                        '/static/dist/js/main.js']

    dash_app = Dash(server=server,
                    external_stylesheets=external_stylesheets,
                    external_scripts=external_scripts,
                    routes_pathname_prefix='/dash/')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "flaskai/flaskai-dec7b-firebase-adminsdk-9o96s-1b92419593.json"
    firebase_admin.initialize_app(options={'databaseURL': 'https://flaskai-dec7b.firebaseio.com'})

    # Fetch Data from firebase online server to pandas df
    df = Fetch_Data_FBserver()
    # print(data.columns.values)

    # Create Dash Layout
    # dash_app.layout = html.Div(id='dash-container', children=[
    #     html.H1('Hello Hassan')
    # ])

    dash_app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),
        html.Div([
            html.Div(
                dcc.Dropdown(
                    id='iotdevice',
                    options=[
                        {'label': name, 'value': name} for name in df['IOT Device'].unique()
                    ],
                    placeholder="Select IOT Device",
                    value='Co2IOT',
                ),
                className='three columns'
            ),
            html.Div(
                html.Label(
                    id='lastreadingdate',
                    title='Last Reading Date Time'
                ),
                className='three columns button'
            ),
            html.Div(
                html.Label(
                    id='isCharging'
                ),
                className='three columns button'
            ),
            html.Div(
                html.Label(
                    id='batterypercent'
                ),
                className='three columns button'
            )
        ],
            className='row'
        ),
        html.Div([
            html.Div(
                children='insert map',
                className='six columns'
            ),
            html.Div(
                children='insert table here',
                className='six columns'
            ),
        ], className='row'),
        html.Div([
            html.Div(
                dcc.Graph(id='example-graph', animate=True),
                className='six columns'
            ),
            html.Div(
                dcc.Graph(id='example-graph1', animate=True),
                className='six columns'
            ),
        ], className='row'),
        html.Div([
            html.Div(
                dcc.Graph(id='example-graph2', animate=True),
                className='six columns'
            ),
            html.Div(
                dcc.Graph(id='example-graph3', animate=True),
                className='six columns'
            ),
        ], className='row')
    ])

    # Initialize callbacks after our app is loaded
    # Pass dash_app as a parameter
    # init_callbacks(dash_app)
    init_callbacks(dash_app)
    return dash_app.server


def Fetch_Data_FBserver():
    rootreference = 'IoT/'
    # child = 'Robot'
    ref = rootreference
    iots = db.reference(ref)
    data = iots.get()
    data_keys = data.keys()
    # data_values = data.values()

    with open('./data/keys.csv', 'w') as f:

        header = "IOT Device"+","+"Unique_Trs_ID"
        f.write(header+"\n")
        for key in data_keys:
            for unique_trs_id, record in data[key].items():
                line = key + "," + unique_trs_id
                f.write(line+"\n")

    with open('./data/details.csv', 'w') as detf:

        dline = {'Unique_Trs_ID': '', 'lat': '', 'lon': '', 'isCharging': '', 'percentage': '',
                 'CO2 %': '', 'Preasure Hg': '', 'Humidity %': '', 'Temperature C': '', 'Speed KM': '', 'date': '', 'time': ''}
        # write the header to CSV file
        w = csv.DictWriter(detf, dline.keys())
        w.writeheader()
        for key in data_keys:
            for Unique_Trs_ID, record in data[key].items():
                dline['Unique_Trs_ID'] = Unique_Trs_ID
                if 'GPS' in record:
                    dline['lat'] = record['GPS']['lat']
                    dline['lon'] = record['GPS']['lon']

                if 'Battery' in record:
                    dline['isCharging'] = record['Battery']['isCharging']
                    dline['percentage'] = record['Battery']['percentage']

                if 'CO2 %' in record:
                    dline['CO2 %'] = record['CO2 %']

                if 'Preasure Hg' in record:
                    dline['Preasure Hg'] = record['Preasure Hg']

                if 'Humidity %' in record:
                    dline['Humidity %'] = record['Humidity %']

                if 'Temperature C' in record:
                    dline['Temperature C'] = record['Temperature C']

                if 'Speed KM' in record:
                    dline['Speed KM'] = record['Speed KM']

                if 'date' in record:
                    dline['date'] = record['date']

                if 'time' in record:
                    dline['time'] = record['time']

                # write to csv file

                w.writerow(dline)

                # the following line is to reset dline,
                dline = {'Unique_Trs_ID': '', 'lat': '', 'lon': '', 'isCharging': '', 'percentage': '',
                         'CO2 %': '', 'Preasure Hg': '', 'Humidity %': '', 'Temperature C': '', 'Speed KM': '', 'date': '', 'time': ''}

        # read the keys and details csv files and merge them.

        dfk = pd.read_csv('./data/keys.csv')
        dfd = pd.read_csv('./data/details.csv')

        data = pd.merge(dfk, dfd)
        del data['Unique_Trs_ID']

        # options = map(data, data)
        # print(options)

    return data


# Note this for callbacks:

#  # Initialize callbacks after our app is loaded
#     # Pass dash_app as a parameter
#     init_callbacks(dash_app)
#
#     return dash_app.server
#
# def init_callbacks(dash_app):
#     @app.callback(
#         # ... Callback input/output
#         )
#     def update_graph():
#         # ... Insert callback stuff here
def init_callbacks(dash_app):
    @dash_app.callback(
        # ... Callback input/output
        [Output(component_id='example-graph', component_property='figure'),
         Output(component_id='example-graph1', component_property='figure'),
         Output(component_id='example-graph2', component_property='figure'),
         Output(component_id='example-graph3', component_property='figure'),
         Output(component_id='lastreadingdate', component_property='children'),
         Output(component_id='isCharging', component_property='children'),
         Output(component_id='batterypercent', component_property='children')],
        [Input(component_id='iotdevice', component_property='value')]
    )
    def update_graph(value):
        # ... Insert callback stuff here
        df = Fetch_Data_FBserver()
        df['date'] = pd.to_datetime(df.date)
        df.sort_values(by='date')

        x = []
        y = []
        # df.loc[df['IOT Device'] == value]
        for index, rows in df.loc[df['IOT Device'] == value].iterrows():
            xvalues = rows.date
            yvalues = rows['CO2 %']
            x.append(xvalues)
            y.append(yvalues)

        title = 'Data Visualization for ' + value
        figure = {
            'data': [
                {'x': x, 'y': y, 'type': 'line', 'name': value},
            ],
            'layout': {
                'title': title,
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'CO2 %'}
            }
        }
        print(df.loc[df['IOT Device'] == value].tail(1))

        lastdate = df['date'].loc[df['IOT Device'] == value].tail(1)
        lasttime = df['time'].loc[df['IOT Device'] == value].tail(1)
        batteycharging = df['isCharging'].loc[df['IOT Device'] == value].tail(1)
        perc = int(df['percentage'].loc[df['IOT Device'] == value].tail(1))

        lastdatetime = str(lastdate) + str(lasttime)
        print(lastdate)
        print(batteycharging)
        return figure, figure, figure, figure, lastdate, batteycharging, perc
