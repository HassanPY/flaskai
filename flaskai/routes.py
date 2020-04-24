# Routes for core Flask app
# import os
from flask import Blueprint, render_template
from flask import current_app as app

flaskaiapp = Blueprint('flaskaiapp', __name__,
                       template_folder='templates',
                       static_folder='static')


@flaskaiapp.route('/')
def home():
    # Landing page."""
    return render_template('dashhome.html',
                           title='Plotly Flask Tutorial.',
                           template='home-template',
                           body='This is an example homepage served with Flask.')
