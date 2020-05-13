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

import os
import firebase_admin
from firebase_admin import db
import pandas as pd
from pandas.io.json import json_normalize
import json


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

    # Fetch Data from firebase online server
    data = Fetch_Data_FBserver()
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
                dcc.Graph(
                    id='example-graph',
                    figure={
                        'data': [
                            {'x': [0, 1, 2, 3], 'y': [0, 7, 1, 2], 'type': 'line', 'name': 'SF'},
                            {'x': [0, 1, 2, 3], 'y': [0, 12, 4, 5],
                                'type': 'line', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Dash Data Visualization'
                        }
                    }
                ),
                className='six columns'
            ),
            html.Div(
                children='insert table here',
                className='six columns'
            ),
        ], className='row')



    ])

    # Initialize callbacks after our app is loaded
    # Pass dash_app as a parameter
    # init_callbacks(dash_app)

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

    with open('./data/details.csv', 'w') as df:
        dheader = "unique_trs_id"+','+"Latitude"+","+"Longitude"+","+"BatteryisCharging"+"," + "Battery Percentage" + \
            ","+"CO2"+","+"Preasure Hg"+","+"Humidity %"+"," + \
                "Temperature C"+"," + "Speed KM"+","+"Date"+","+"Time"
        df.write(dheader+"\n")

        dline = {'unique_trs_id': '', 'lat': '', 'lon': '', 'isCharging': '', 'percentage': '',
                 'CO2 %': '', 'Preasure Hg': '', 'Humidity %': '', 'Temperature C': '', 'Speed KM': '', 'date': '', 'time': ''}

        def write_to_csv_file():
            [df.write('{0},'.format(value)) for key, value in dline.items()]
            df.write("\n")

        for key in data_keys:
            for unique_trs_id, record in data[key].items():
                dline['unique_trs_id'] = unique_trs_id
                if 'GPS' in record:
                    dline['lat'] = record['GPS']['lat']
                    dline['lon'] = record['GPS']['lon']
                    write_to_csv_file()
                elif 'Battery' in record:
                    dline['isCharging'] = record['Battery']['isCharging']
                    dline['percentage'] = record['Battery']['percentage']
                    write_to_csv_file()
                elif 'CO2 %' in record:
                    dline['CO2 %'] = record['CO2 %']
                    write_to_csv_file()
                elif 'Preasure Hg' in record:
                    dline['Preasure Hg'] = record['Preasure Hg']
                    write_to_csv_file()
                elif 'Humidity %' in record:
                    dline['Humidity %'] = record['Humidity %']
                    write_to_csv_file()
                elif 'Temperature C' in record:
                    dline['Temperature C'] = record['Temperature C']
                    write_to_csv_file()
                elif 'Speed KM' in record:
                    dline['Speed KM'] = record['Speed KM']
                    write_to_csv_file()
                elif 'date' in record:
                    dline['date'] = record['date']
                    write_to_csv_file()
                elif 'time' in record:
                    dline['time'] = record['time']
                    write_to_csv_file()
                else:
                    print('else is working ######')
                # the following line is to reset dline,
                # location of the line to be confirmed
                dline = {'unique_trs_id': '', 'lat': '', 'lon': '', 'isCharging': '', 'percentage': '',
                         'CO2 %': '', 'Preasure Hg': '', 'Humidity %': '', 'Temperature C': '', 'Speed KM': '', 'date': '', 'time': ''}

    with open('./data/iotdata .json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    df = pd.read_json('./data/iotdata.json')
    # print(json_normalize(df, max_level=0))
    # print(df.to_json(orient='split'))

    # print(df.to_json(orient='index'))
    df.to_csv('./data/iotdata.csv')

    return df


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
