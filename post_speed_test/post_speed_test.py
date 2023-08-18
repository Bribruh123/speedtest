




import requests
import datetime
import time

dt_obj = datetime.datetime.now()
last_time = int(dt_obj.timestamp() * 1000)

while True:


    dt_obj = datetime.datetime.now()
    # dt_obj = datetime.datetime.now().strptime('20.12.2016 09:38:42,76',
    #    '%d.%m.%Y %H:%M:%S,%f')
    millisec = int(dt_obj.timestamp() * 1000)
    if millisec - last_time > 2000:
        print("PASSED")
        last_time = millisec
        url = "https://routerlogin.net/func.cgi?/QOS_dynamic.htm %20timestamp={}".format(last_time)

        payload = 'submit_flag=ookla_speedtest&hid_trend_micro_enable=&hid_bandwidth_type=&hid_trend_micro_uplink=&hid_trend_micro_downlink=&hid_first_flag=&hid_detect_database=&hid_improve_service=&hid_update_agreement=0&hid_cancel_speedtest=0&dynamic_qos_enable=on&qosSetting=1&downlink_value=&uplink_value=&AutoUpdateEnable=0&help_improve=0'
        headers = {
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
          'Accept-Language': 'en-US,en;q=0.9',
          'Authorization': 'Basic YWRtaW46ZDY5YWRyUFJyUTl4QFlI',
          'Cache-Control': 'max-age=0',
          'Connection': 'keep-alive',
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': 'optimizelyEndUserId=oeu1689251762689r0.9599328553140711; _gcl_au=1.1.158394634.1689251763; _ce.s=v~bf19a04049373559b431d83d3da3cf08bdec976e~lcw~1689251763343~vpv~0~lcw~1689251763344; _ga=GA1.2.970939720.1689251764; _ga_FJW3T6WEP0=GS1.1.1689251763.1.0.1689251779.0.0.0; auth_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIyNjQyNDciLCJpc3MiOiJ3d3cubmV0Z2Vhci5jb20iLCJzdWIiOiIobnVsbCkifQ==.fe6918677fac63e5f6a72d2c5124da3421ddf5a1b243d17d39981122561dab74',
          'Origin': 'https://routerlogin.net',
          'Referer': 'https://routerlogin.net/QOS_dynamic.htm',
          'Sec-Fetch-Dest': 'iframe',
          'Sec-Fetch-Mode': 'navigate',
          'Sec-Fetch-Site': 'same-origin',
          'Sec-Fetch-User': '?1',
          'Upgrade-Insecure-Requests': '1',
          'sec-ch-ua-mobile': '?0'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(response.text)
        time.sleep(4)
        url_check = "https://routerlogin.net/QOS_speedtest_result.htm"

        payload = {}
        headers = {
          'Accept': '*/*',
          'Accept-Language': 'en-US,en;q=0.9',
          'Authorization': 'Basic YWRtaW46ZDY5YWRyUFJyUTl4QFlI',
          'Connection': 'keep-alive',
          'Cookie': 'optimizelyEndUserId=oeu1689251762689r0.9599328553140711; _gcl_au=1.1.158394634.1689251763; _ce.s=v~bf19a04049373559b431d83d3da3cf08bdec976e~lcw~1689251763343~vpv~0~lcw~1689251763344; _ga=GA1.2.970939720.1689251764; _ga_FJW3T6WEP0=GS1.1.1689251763.1.0.1689251779.0.0.0; auth_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIyODg0OTEiLCJpc3MiOiJ3d3cubmV0Z2Vhci5jb20iLCJzdWIiOiIobnVsbCkifQ==.b1f00661815162cb88f84cfe92f9d0b75ed622c34f87f6beb007f645e43e8a1e',
          'Referer': url,
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-origin',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
          'X-Requested-With': 'XMLHttpRequest',
          'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"'
        }

        response = requests.request("GET", url_check, headers=headers, data=payload,  verify=False)

        print(response.text)
    print(last_time, millisec)
    time.sleep(5)

