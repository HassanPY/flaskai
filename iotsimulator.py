import random
# import time
from datetime import date, datetime
import time
import os
# import urllib3
import firebase_admin
from firebase_admin import db  # , credentials
# http = urllib3.PoolManager()
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "flaskai/flaskai-dec7b-firebase-adminsdk-9o96s-1b92419593.json"

firebase_admin.initialize_app(
    options={'databaseURL': 'https://flaskai-dec7b.firebaseio.com'})
rootreference = 'IoT/'
records = {}


while True:

    iot_point = random.choice(["Robot", "IOTdevice", "Drone"])
    device_no = iot_point + str(random.randint(1, 5))
    reading_temp = str(random.randint(10, 55))
    reading_co = str(random.randint(24, 30))
    reading_hg = str(random.randint(20, 40))
    reading_humid = str(random.randint(10, 100))
    reading_speed = str(random.randint(0, 5))
    reading_isCharging = str(random.choice([True, False]))
    reading_percentage = str(random.randint(1, 100))
    reading_lat = random.uniform(23.14355, 25.78953)
    reading_lon = random.uniform(52.73056, 56.34199)

    records['Temperature C'] = reading_temp
    records['CO2 %'] = reading_co
    records['Preasure Hg'] = reading_hg
    records['Speed KM'] = reading_speed
    records['Humidity %'] = reading_humid
    records['Battery'] = {"isCharging": reading_isCharging, "percentage": reading_percentage}
    records['Unique Id'] = "fromsimulator7788 "
    records['GPS'] = {"lat": reading_lat, "lon": reading_lon}

    current_date = date.today()
    current_time = datetime.now().time()
    records['date'] = current_date.strftime("%d/%m/%y")
    records['time'] = current_time.strftime("%H:%M")

    ref = rootreference + device_no
    iots = db.reference(ref)

    child = iots.push(records)

    print(device_no, current_date, current_time)

    time.sleep(600)
