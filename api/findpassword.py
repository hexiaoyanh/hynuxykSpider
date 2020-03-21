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
        if self.nanyue is True:
            url = url = "http://59.51.24.41/yhxigl.do?method=resetPasswd"
        else:
            url = "http://59.51.24.46/hysf/yhxigl.do?method=resetPasswd"
        data = {
            "account": self.username,
            "sfzjh": self.idcardnum
        }
        data = requests.post(url=url, data=data)
        try:
            msg = re.search("alert\('.*?'\)", data.text).group(0)
            if msg == "alert('密码已重置为身份证号的后六位')":
                return {
                    "Code": 1,
                    "Msg": "密码已重置为身份证号的后六位"
                }
        except AttributeError:
            return {
                "Code": -1,
                "Msg": "学号或身份证号错误"
            }

    def __init__(self, username, idcardnum, nanyue):
        self.username = username
        self.idcardnum = idcardnum
        self.nanyue = nanyue
