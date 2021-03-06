from datetime import date, time, datetime
from geojson import Point, Feature, FeatureCollection
from flaskai import app
from flaskai.forms import StockPriceForm as form
from flask import render_template, flash, request, url_for, redirect
import json
import firebase_admin
from firebase_admin import db, credentials
import os
import flask
import firebase_admin
import folium

# imports for Video streaming

from flaskai.singlemotiondetector import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
import threading
import argparse
import imutils
import time
import cv2

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "flaskai/flaskai-dec7b-firebase-adminsdk-9o96s-1b92419593.json"

#cred = credentials.Cert('flaskai-dec7b-firebase-adminsdk-9o96s-1b92419593.json')
firebase_admin.initialize_app(options={'databaseURL': 'https://flaskai-dec7b.firebaseio.com'})

MAPBOX_ACCESS_KEY = 'pk.eyJ1IjoiaGFzc2FuaWgiLCJhIjoiY2pqcjhsZTV1NjNhcjNrdGU3YzRjYXcweSJ9.1oFwx11tzzFVOyAyfojwrg'
# _ensure_company is internal helper function

# Creat Map Object, Dubai Location 25.2048° N, 55.2708° E
m = folium.Map(location=[25.2048, 55.2708], zoom_start=10)


@app.route("/test")
def test():
    return render_template('test.html')


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')


@app.route("/map", methods=['POST', 'GET'])
def map():
    child = ""
    if request.method == "POST":

        req = request.form
        child = req.get("Select IoT Device")
        print(child)
        # print(request.url)

        # return redirect(request.url)
    rootreference = 'IoT/'
    # child = 'Robot'
    ref = rootreference
    iots = db.reference(ref)
    data = iots.get()
    data_keys = data.keys()
    # data_values = data.values()
    # print(type(data_values))
    if (child == "" or child == "All"):
        for key in data_keys:
            for _, record in data[key].items():

                if 'GPS' in record:
                    lat = record['GPS']['lat']
                    lon = record['GPS']['lon']
                    # Create markers
                    # print(child)
                    folium.Marker([lat, lon],
                                  popup=record,
                                  toolretip=key).add_to(m)
                    # icon=folium.Icon(color='green', icon='wifi')).add_to(m)
        m.save('flaskai/static/mapfolium.html')

    else:
        # print(child)

        mchild = folium.Map(location=[25.2048, 55.2708], zoom_start=10)
        records = data[child]
        # print(record['GPS'])
        for _, record in records.items():
            if 'GPS' in record:
                lat = record['GPS']['lat']
                lon = record['GPS']['lon']

            # Create markers
            folium.Marker([lat, lon],
                          popup=record,
                          toolretip=child).add_to(mchild)
            # icon=folium.Icon(color='green', icon='wifi')).add_to(m)
    # Generate Map
        # mchild.save('flaskai/static/mapfolium.html')
        mchild.save('flaskai/static/mapfolium.html')
    return render_template('map.html', data_keys=data_keys, child=child)


@app.route("/about")
def about():
    return render_template('template.html')


@app.route('/device/<iot_name>', methods=['POST', 'GET'])
def device(iot_name):
    rootreference = 'iot/'
    node_name = iot_name
    ref = rootreference + node_name
    iots = db.reference(ref)
    reading = request.args.get('value')
    records = {}
    records['reading'] = reading
    current_date = date.today()
    current_time = datetime.now().time()
    records['date'] = current_date.strftime("%d/%m/%y")
    records['time'] = current_time.strftime("%H:%M")
    #records['node_name'] = iot_name
    #json_records = json.dumps(records)

    child = iots.push(records)
    flash('records has been added', 'success')
    return render_template('iot.html', records=records)


@app.route('/company', methods=['POST', 'GET'])
def company():
    rootreference = 'stockprices/'
    companyref = 'amazon/'
    yearref = '2018'
    ref = rootreference + companyref + yearref
    stprices = db.reference(ref)

    records = '{"date": "08/08/2018", "open": 777, "low": 888, "high": 999, "volume": 89898989}'
    json_records = json.loads(records)
    child = stprices.push(json_records)
    flash('records has been added', 'success')
    return render_template('home.html', records=json_records)


@app.route('/read', methods=['GET'])
def read():

    rootreference = 'stockprices/'
    companyref = 'amazon/'
    yearref = '2018'
    ref = rootreference + companyref + yearref
    #stprices = db.reference(ref)
    results = db.reference(ref).get(etag=False)
    singlerecord = db.reference(ref).child('-LGTWq-_imBMsGjgxIcb').get(etag=False)
    if request.method == 'GET':
        form.stockdate.data = singlerecord['date']
        form.openprice.data = singlerecord['open']
        form.lowprice.data = singlerecord['low']
        form.highprice.data = singlerecord['high']
        form.volume.data = singlerecord['volume']

    return render_template('data.html', results=results, form=form)


@app.route('/update', methods=['POST', 'GET'])
def update():
    rootreference = 'stockprices/'
    companyref = 'amazon/'
    yearref = '2018'
    childref = '-LGTWk0yZ_Xt448qFq3m'
    newvalue = {"date": "06/06/2222", "open": 2000, "low": 1900, "high": 2200, "volume": 555555}
    ref = rootreference + companyref + yearref
    Reference = db.reference(ref)
    Reference.child(childref).update(newvalue)
    return render_template('update.html', childref=childref)


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    rootreference = 'stockprices/'
    companyref = 'amazon/'
    yearref = '2018'
    childref = '-LGUE2Y3_nmZ7VaoxoVJ'
    ref = rootreference + companyref + yearref
    Reference = db.reference(ref)
    Reference.child(childref).delete()
    return render_template('delete.html', childref=childref)


# Video Streaming Code *********
# To run video streaming run (Dont forget to start venv):
# python3 webstreaming.py --ip 0.0.0.0 --port 8000
# at browser go to : http://0.0.0.0:8000/dronevideo
