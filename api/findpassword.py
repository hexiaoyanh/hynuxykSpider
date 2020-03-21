"""
@File : findpassword.py
@Author: Mika
@Date : 2020/3/21
@Desc :
"""
import requests
import re


class findpassword:

    def resetPasswd(self):
        url = "http://59.51.24.46/hysf/yhxigl.do?method=resetPasswd"
        data = {
            "account": self.username,
            "sfzjh": self.idcardnum
        }
        data = requests.post(url=url, data=data)
        msg = re.search("alert\('.*?'\)", data.text).group(0)
        if msg == "alert('密码已重置为身份证号的后六位')":
            return {
                "Code": 1,
                "Msg": "密码已重置为身份证号的后六位"
            }
        else:
            return {
                "Code": -1,
                "Msg": "学号或身份证号错误"
            }

    def findpassword(self):
        return self.resetPasswd()

    def __init__(self, username, idcardnum):
        self.username = username
        self.idcardnum = idcardnum
