import json

import requests
from bs4 import BeautifulSoup



class querykb():
    url = None

    def postrequests(self):
        print(self.url, self.cookie)
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
                    if k != 2:
                        temp = {strs: soup.find(id=strs).text.replace('\xa0', '')}
                    else:
                        s = str(soup.find(id=strs))
                        s = s.replace("<div id=\"{0}\" style=\"display: none;\">".format(strs), '')
                        s = s.replace("</div>", '')
                        s = s.replace("<br/>", ' ')
                        s = s.replace("<nobr>", " ")
                        s = s.replace("</nobr>", ' ')
                        s = s.replace('\xa0', '')
                        temp = {strs: s}
                    week.append(temp)
                data.append(week)
        return json.dumps(data, ensure_ascii=False)

    def queryallkb(self, date, week):
        if self.nanyue is True:
            self.url = self.url = "http://59.51.24.41/tkglAction.do?method=goListKbByXs&istsxx=no&xnxqh={0}&zc={1}&xs0101".format(
                date, week)
        else:
            self.url = "http://59.51.24.46/hysf/tkglAction.do?method=goListKbByXs&istsxx=no&xnxqh={0}&zc={1}&xs0101".format(
                date, week)
        soup = self.postrequests()
        return self.dealdata(soup)

    def __init__(self, cookie, nanyue):
        self.cookie = {'JSESSIONID': cookie}
        self.nanyue = nanyue
