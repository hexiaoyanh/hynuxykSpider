import requests
from bs4 import BeautifulSoup

from api.login import login


class querykb(login):
    url = "http://59.51.24.46/hysf/tkglAction.do?method=goListKbByXs&istsxx=no&xnxqh=2019-2020-1&zc=&xs0101"

    def postrequests(self):
        data = requests.post(url=self.url, cookies=self.cookie)
        soup = BeautifulSoup(data.text, 'html.parser')
        return soup

    def dealdata(self, soup):
        table = soup.find(id='kbtable').find_all('tr')[1:]
        table = table[:-1]
        #for i in table:
        td = table[0].find_all('td')
        print(td[5].find_all('div')[1])


    def queryallkb(self):
        soup = self.postrequests()
        self.dealdata(soup)

    def __init__(self, *args):
        if len(args) == 2:
            super().__init__(args[0], args[1])
        else:
            self.cookie = args[0]
