import speedtest
import datetime
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import requests
import json
from decimal import Decimal

# Collect data from router and parse
def get_netgear_speeds(dictData):

    # Router speeds
    upSpeed = float(dictData['upSpeed'].split(" ")[0])
    downSpeed= float(dictData['downSpeed'].split(" ")[0]) 
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
    for device in dictData['devices']:
        print(device['deviceName'])
        point = (
          Point("device_speeds")
          .tag("deviceName", device['deviceName'])
          .field("deviceName", device['deviceName'])  
          .field("upSpeed", float(device['upSpeed'].split(" ")[0]))
          .field("downSpeed", float(device['downSpeed'].split(" ")[0]))
          .field("priority", device['priority'])
          .field("connType", device['connType'])
          .field("ip", device['ip'])
          .field("deviceModel", device['deviceModel'])
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
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    dt_obj = datetime.datetime.now().strptime('20.12.2016 09:38:42,76',
       '%d.%m.%Y %H:%M:%S,%f')
    millisec = int(dt_obj.timestamp() * 1000)
    print(millisec)

    # Https request to pull QoS data from router
    url = "https://routerlogin.net/refresh_dev.htm?ts={}".format(millisec)
    payload = {}
    headers = {
      'Authorization': 'Basic YWRtaW46ZDY5YWRyUFJyUTl4QFlI',
      'Cookie': 'auth_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIyMDI1MDAiLCJpc3MiOiJ3d3cubmV0Z2Vhci5jb20iLCJzdWIiOiIobnVsbCkifQ==.62dd719e0331a4c39b6ce8bb7bf3e8b9b9847c99af8cb235fdab45eb8fb5d3da'
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    print(response.text)
    dictData= json.loads(response.text)

    # parse data from router
    netgear_points = get_netgear_speeds(dictData)

    # parse data from router
    device_points = get_device_speeds(dictData)

    host_points = get_agent_speeds()
    
    write_api = write_client.write_api(write_options=SYNCHRONOUS)
    bucket="LOGS"
    write_api.write(bucket=bucket, org=org, record=netgear_points)
    write_api.write(bucket=bucket, org=org, record=device_points)
    write_api.write(bucket=bucket, org=org, record=host_points)

    # Rest 10 seconds
    time.sleep(10)

