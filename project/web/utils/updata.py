import json
import re
import urllib.request


def getData():
    url = "http://61.152.117.25/SqlHelper/passenger/PassengerInfo.asmx/QueryRealtimeInfo?callback" \
          "=jQuery17209489305473286322_1604326222192&username=dfw&password=eastday&district=0&_=1604326224091 "
    http_request = urllib.request.Request(url=url, method='GET')
    http_response = urllib.request.urlopen(http_request).read()
    http_entity = http_response.decode('utf8')
    result1 = re.findall(r'"([\s\S]*)"', http_entity)
    result1 = result1[0].replace("\'", "\"")
    data = json.loads(result1)
    return data
