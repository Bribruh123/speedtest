import requests

url = "https://routerlogin.net/refresh_dev.htm?ts=1693675199748"

payload = {}
headers = {
  'Authorization': 'Basic YWRtaW46ZDY5YWRyUFJyUTl4QFlI'
}

session = requests.Session()
print(session.cookies.get_dict())

response = session.request("GET", url, headers=headers, data=payload, verify=False)

print(response.text)
print(session.cookies.get_dict())