import requests
from bs4 import BeautifulSoup

from .ocr import ocr


class login:
    cookie = None
    Msg = ""
    ############################################login begin############################################
    def setcookie(self):
        url = "http://59.51.24.46/hysf/"
        data = requests.get(url=url)
        JSESSIONID = data.cookies['JSESSIONID']
        self.cookie = dict(JSESSIONID=JSESSIONID)

    def getverificationcode(self):
        url = "http://59.51.24.46/hysf/verifycode.servlet"
        data = requests.get(url=url, cookies=self.cookie)
        img2str = ocr.img2str(data.content)
        return img2str.dealimg()

    def login(self):
        self.setcookie()
        code = self.getverificationcode()
        payload = {
            'USERNAME': self.username,
            'PASSWORD': self.password,
            'useDogCode': '',
            'useDogCode': '',
            'RANDOMCODE': code,
            'x': '39',
            'y': '10'
        }
        url = "http://59.51.24.46/hysf/Logon.do?method=logon"
        data = requests.post(url=url, cookies=self.cookie, data=payload)
        bs = BeautifulSoup(data.text,'html.parser')
        error = bs.find(id='errorinfo')
        if error is not None:
            return error.text
        else:
            self.getmsg()
            return "OK"

    def getmsg(self):
        url = "http://59.51.24.46/hysf/Logon.do?method=logonBySSO"
        data = requests.get(url=url, cookies=self.cookie)

    ############################################login end############################################
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.Msg = self.login()
