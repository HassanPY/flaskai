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
