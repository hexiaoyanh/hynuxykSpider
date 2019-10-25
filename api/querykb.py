import json

import requests
from bs4 import BeautifulSoup

from api.login import login


class querykb(login):
    url = None

    def postrequests(self):
        data = requests.post(url=self.url, cookies=self.cookie)
        soup = BeautifulSoup(data.text, 'html.parser')
        return soup

    def dealdata(self, soup):
        data = []
        for i in range(1, 6):
            for j in range(1, 8):
                week = []
                for k in range(1, 4):
                    strs = "{0}-{1}-{2}".format(i, j, k)
                    temp = {strs: soup.find(id=strs).text.replace('\xa0', '')}
                    week.append(temp)
                data.append(week)
        return json.dumps(data,ensure_ascii=False)

    def queryallkb(self, date, week):
        self.url = "http://59.51.24.46/hysf/tkglAction.do?method=goListKbByXs&istsxx=no&xnxqh={0}&zc={1}&xs0101".format(
            date, week)
        soup = self.postrequests()
        return self.dealdata(soup)

    def __init__(self, *args):
        if len(args) == 2:
            super().__init__(args[0], args[1])
        else:
            self.cookie = args[0]
