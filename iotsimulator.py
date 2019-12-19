import random
import time
import urllib3

http = urllib3.PoolManager()

i=1
while True:

    iot_point = random.choice(["tempIOT", "coIOT", "hgIOT", "humidIOT"])

    device_no = iot_point + str(random.randint(1,100))
    reading_temp = str(random.randint(10,55))
    reading_co = str(random.randint(24,30))
    reading_hg = str(random.randint(20,40))
    reading_humid = str(random.randint(10,100))
    domain = "http://127.0.0.1:5000/"
    if iot_point == "tempIOT":
        record = "device/" + device_no + "?" + "value=" + reading_temp
    elif iot_point == "coIOT":
        record = "device/" + device_no + "?" + "value=" + reading_co
    elif iot_point == "hgIOT":
        record = "device/" + device_no + "?" + "value=" + reading_hg
    else :
        record = "device/" + device_no + "?" + "value=" + reading_humid

    url = domain + record

    # r = http.request('POST','http://httpbin.org/post', fields={'hello': 'world'})
    r = http.request('POST',url)
    print (i)
    i=i+1
    time.sleep(60)

p
