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
    s = speedtest.Speedtest(secure=True)
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

    # Https request to pull QoS data from router
    url = "https://routerlogin.net/refresh_dev.htm?ts={}".format(millisec)

    payload = {}
    headers = {
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Accept-Language': 'en-US,en;q=0.9',
      'Authorization': 'Basic YWRtaW46ZDY5YWRyUFJyUTl4QFlI',
      'Connection': 'keep-alive',
      'Cookie': 'optimizelyEndUserId=oeu1689251762689r0.9599328553140711; _gcl_au=1.1.158394634.1689251763; _ce.s=v~bf19a04049373559b431d83d3da3cf08bdec976e~lcw~1689251763343~vpv~0~lcw~1689251763344; _ga=GA1.2.970939720.1689251764; _ga_FJW3T6WEP0=GS1.1.1689251763.1.0.1689251779.0.0.0; auth_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIyOTAxODYiLCJpc3MiOiJ3d3cubmV0Z2Vhci5jb20iLCJzdWIiOiIobnVsbCkifQ==.dd27842b6d81083ddea2ffdc6fa85af621e0a73a9743ad118dc081754ff0fe7f; auth_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIyODk1MzMiLCJpc3MiOiJ3d3cubmV0Z2Vhci5jb20iLCJzdWIiOiIobnVsbCkifQ==.f601c8b95bb687546e4c5c99c07c2dfc4e1d4bee1d186e9e2f161ea46e642dbe',
      'Referer': 'https://routerlogin.net/QOS_list_device.htm',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
      'X-Requested-With': 'XMLHttpRequest',
      'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"'
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

