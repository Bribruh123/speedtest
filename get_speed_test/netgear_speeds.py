import speedtest
import datetime
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import requests
import json
import os
import base64

# Collect data from router and parse
def get_netgear_speeds(dictData):

    # Router speeds
    downSpeed = float(response.text.split(";")[1])/1000000
    upSpeed = float(response.text.split(";")[0])/1000000
    netgear_point = (
        Point("Netgear_speeds")
        .tag("tagname1", "tagvalue1")
        .field("upspeed", upSpeed)
        .field("downspeed", downSpeed)
    )
    return netgear_point
    

def get_device_speeds(dictData):
    points = []
    # Device speeds
    for device in dictData['connDevices']:
        print(device['name'])
        point = (
            Point("device_speeds")
        .tag("deviceName", device['name'])
        .field("deviceName", device['name'])  
         .field("upSpeed", float(device['uploadSpeedStr'].split(" ")[0]))
       .field("downSpeed", float(device['downloadSpeedStr'].split(" ")[0]))
          .field("priority", device['priorityStr'])
          .field("connType", device['connection'])
          .field("ip", device['ip'])
          .field("deviceModel", device['model'])
          .field("mac", device['mac'])
        )
        points.append(point)
    return points

def get_agent_speeds():
    s = speedtest.Speedtest()
    downspeed = round((round(s.download()) / 1048576), 2)
    upspeed = round((round(s.upload()) / 1048576), 2)
    point = (
        Point("host_agent_speeds")
        .tag("tagname1", "tagvalue1")
        .field("upspeed", upspeed)
        .field("downspeed", downspeed)
    )
    return point

token = "veryverysecuretoken"
org = "SPEEDTEST"
url = "http://influxdb:8086"
write_client = InfluxDBClient(url=url, token=token, org=org)

while True:

    # Collect current timestamp (miliseconds)
    dt_obj = datetime.datetime.now()
    millisec = int(dt_obj.timestamp() * 1000)
    print(millisec)

    # # Https request to pull QoS data from router
    # url_router = "https://routerlogin.net/refresh_dev.htm"

    router_username = os.environ["ROUTER_USERNAME"]
    router_password = os.environ["ROUTER_PASSWORD"]
    encoded = base64.b64encode("{}:{}".format(router_username, router_password).encode("ascii"))

    payload = {}
    headers = {
      'Authorization': 'Basic {}'.format(encoded.decode("ascii"))
    }


    url = "http://routerlogin.net/"

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    print(response)
    print(response.headers)
    if 'Set-Cookie' in response.headers:
        headers['Cookie'] = response.headers['Set-Cookie'].split(";")[0]
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        print(response)

    url = "http://routerlogin.net/ajax/devices_table_result"

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)


    dictData= json.loads(response.text)
    print(dictData)
    device_points = get_device_speeds(dictData)

    url = "http://routerlogin.net/ajax/devices_table_result"

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    url = "http://routerlogin.net/qos_uplink_check.php"


    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print(response)
    # # parse data from router
    netgear_points = get_netgear_speeds(response.text)
    host_points = get_agent_speeds()
    
    write_api = write_client.write_api(write_options=SYNCHRONOUS)
    bucket="LOGS"
    write_api.write(bucket=bucket, org=org, record=netgear_points)
    write_api.write(bucket=bucket, org=org, record=device_points)
    write_api.write(bucket=bucket, org=org, record=host_points)

    # Rest 10 seconds
    time.sleep(300)

