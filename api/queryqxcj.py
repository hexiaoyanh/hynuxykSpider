############################################查询平时成绩 begin###################################
import re

import requests
from bs4 import BeautifulSoup
from flask import jsonify


def querypscj(urls, cookie):
    urls = "http://59.51.24.46" + re.search("'.*'", urls).group(0).replace("'", "")
    data = requests.get(url=urls, cookies=cookie)
    soup = BeautifulSoup(data.text, 'html.parser')
    data = soup.find(id="mxhDiv")
    data = data.find_all('td')
    return jsonify([data[0].text, data[1].text, data[4].text, data[5].text, data[6].text])

############################################查询平时成绩 end###################################
