import speedtest
import datetime
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import requests
import json
import os
import base64
from bs4 import BeautifulSoup

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

def get_netgear_logs(response):
    bucket = "LOGS"
    org = "SPEEDTEST"
    token = "veryverysecuretoken"
    url = "http://influxdb:8086"

    read_client = InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    query_api = read_client.query_api()
    query = 'from(bucket:"LOGS")\
    |> range(start: -10m)\
    |> filter(fn:(r) => r._measurement == "netgear_logs")'
    result = query_api.query(org=org, query=query)
    results = []
    last_log = None
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    if len(results) > 0:
        last_log = results[len(results)-1][1]
        print("last_logs", results)
    else:
        last_log = None
    logs = []
    log_points = []
    # print()
    found =False
    for line in response.text.split("\n"):

      if found:
        if "</textarea>" in line:
          break
        else:
          logs.append(line)

      elif '<TEXTAREA NAME="log_detail"' in line:
        found = True
        continue

    for log in logs:
      if last_log and log != last_log:  
          print(log)
          point = (
            Point("netgear_logs")
            .field("log", str(log))
          )
          log_points.append(point)
      if not last_log:
        print(log)
        point = (
            Point("netgear_logs")
            .field("log", str(log))
          )
        log_points.append(point)
      else:
        break


    print(log_points)
    return log_points



token = "veryverysecuretoken"
org = "SPEEDTEST"
url = "http://influxdb:8086"
write_client = InfluxDBClient(url=url, token=token, org=org)

def get_netgear_vpn_and_mesh(response):
    lines = response.text.split("\n")
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all("table")
    table_str = str(tables[1])

    soup = BeautifulSoup(table_str, 'html.parser')
    data = soup.find_all("span")

    headers= []
    filtered = []
    for i in range(len(data)):
      dp_string = str(data[i]).split(">")[1].split("<")[0]
      if dp_string:
        filtered.append(dp_string)

    headers = filtered[0:6]
    print(headers)

    mesh_devs = []

    mesh_dev_cnt = 1
    i = 6
    while i < len(filtered):
      # print(i)
      # print(filtered[i])
      if filtered[i].isnumeric() and int(filtered[i]) == mesh_dev_cnt:
        print(filtered[i:i+10])
        mesh_devs.append(filtered[i:i+10])
        i = i +10
        mesh_dev_cnt = mesh_dev_cnt +1
      else:
        i = i +1

    i = len(filtered)-4
    vpn_start = 0
    while i >= 0:
      # print(filtered[i])
      if filtered[i] == "Device Name":
        # print(filtered[i])
        vpn_start= i
        break
      i = i -4

    vpn_headers = filtered[vpn_start:vpn_start+4]
    vpn_clients = []
    print(vpn_headers)
    i = vpn_start +4
    while i < len(filtered):
      # print(i)
      # print(filtered[i])
      print(filtered[i:i+4])
      vpn_clients.append(filtered[i:i+4])
      i = i +4

    mesh_points = []
    for item in mesh_devs:
        point = (
        Point("mesh_devices")
        .tag("number", item[0])
        .field("Device Name", item[1])
        .field("IP", item[6])
        .field("Connection Type", item[7])
        .field("Connected Mesh Device", item[8])
        .field("Backhaul Status", item[9])
        )
        mesh_points.append(point)

    vpn_points = []
    for item in vpn_clients:
        point = (
        Point("vpn_clients")
        .tag("Device Name", item[0])
        .field("Device Name", item[0])
        .field("Remote IP Address", item[1])
        .field("Local IP Address", item[2])
        .field("Connection Time", item[3])
        )
        vpn_points.append(point)

    return(mesh_points, vpn_points)

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


    #logs

    url = "http://routerlogin.net/FW_log.htm"

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    log_points = get_netgear_logs(response)

    #mesh and vpn


    url = "http://routerlogin.net/DEV_device_DI_iQoS.htm"

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    mesh_points, vpn_points = get_netgear_vpn_and_mesh(response)

    #devices

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
    write_api.write(bucket=bucket, org=org, record=mesh_points)
    write_api.write(bucket=bucket, org=org, record=vpn_points)
    for point in log_points:
        write_api.write(bucket=bucket, org=org, record=point)

    # Rest 10 seconds
    time.sleep(300)

