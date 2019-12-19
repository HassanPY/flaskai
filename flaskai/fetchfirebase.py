import firebase_admin
from firebase_admin import db
import os
import folium


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "flaskai-dec7b-firebase-adminsdk-9o96s-1b92419593.json"

# cred = credentials.Cert('flaskai-dec7b-firebase-adminsdk-9o96s-1b92419593.json')
firebase_admin.initialize_app(
    options={'databaseURL': 'https://flaskai-dec7b.firebaseio.com'})

# Creat Map Object, Dubai Location 25.2048° N, 55.2708° E
m = folium.Map(location=[25.2048, 55.2708], zoom_start=10)


rootreference = 'IoT/'
# child = 'Robot'
ref = rootreference  # + child
iots = db.reference(ref)
data = iots.get()
data_keys = data.keys()
# data_values = data.values()
# print(type(data_values))
for key in data_keys:
    for _, record in data[key].items():
        # print(key)
        # print(record)
        # print(record['GPS']['lat'], record['GPS']['lon'], record['date'],
        # record['time'])
        if 'GPS' in record:
            lat = record['GPS']['lat']
            lon = record['GPS']['lon']

            # Create markers
            folium.Marker([lat, lon],
                          popup=record,
                          tooltip=key).add_to(m)
            # icon=folium.Icon(color='green', icon='wifi')).add_to(m)
# Generate Map
m.save('map.html')
