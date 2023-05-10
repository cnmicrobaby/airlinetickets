import re
import requests

# 返回全国城市的信息
url = "http://webresource.c-ctrip.com/code/cquery/resource/address/flight/flight_new_poi_gb2312.js?"
response = requests.get(url, verify=False)
station = re.findall("([\u4e00-\u9fa5]+)\\(([A-Z]+)\\)", response.text)
stations = dict(station)