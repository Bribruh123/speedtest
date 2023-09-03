import requests
import json

url = "http://admin:admin@grafana:3000/api/auth/keys"

payload = json.dumps({
  "name": "apikeycurl",
  "role": "Admin"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

try:
  key = json.loads(response.text)['key']


  url = "http://grafana:3000/api/datasources"

  payload = json.dumps({
    "id": None,
    "name": "InfluxDB",
    "type": "influxdb",
    "typeName": "InfluxDB",
    "access": "proxy",
    "url": "http://influxdb:8086",
    "user": "",
    "database": "",
    "basicAuth": False,
    "isDefault": False,
    "jsonData": {
      "dbName": "LOGS",
      "httpHeaderName1": "Authorization"
    },
    "readOnly": False,
    "secureJsonData": {
      "httpHeaderValue1": "Token veryverysecuretoken"
    }
  })



  headers = {
    'Authorization': 'Bearer {}'.format(key),
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  print(response.text)
except Exception as e:
  print("Failed, Created Already")


