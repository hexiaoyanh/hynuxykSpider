"""
@File : ntce.py
@Author: Mika
@Date : 2020/3/27
@Desc :
"""
import base64
import re
from bs4 import BeautifulSoup
import requests, random


class ntce:

    def get_img(self):
        try:
            headers = {
                'Connection': 'keep - alive',
                'Host': 'search.neea.edu.cn',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            }
            get_url = "http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryCond&pram=results&community=Home&sid=2nasVMoohJ6cFnsQEIjGYmh"

            response = requests.get(get_url, headers=headers)
            img_url = "http://search.neea.edu.cn/Imgs.do?act=verify&t=" + str(random.random())
            headers = {
                'Connection': 'keep - alive',
                'Referer': 'http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryCond&pram=results&community=Home&sid=2nasVMoohJ6cFnsQEIjGYmh',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            }
            img = requests.get(img_url, timeout=None, cookies=response.cookies, headers=headers)
            image_base64 = str(base64.b64encode(img.content), encoding='utf-8')
            return {
                "code": "1",
                "cookies": img.cookies['verify'],
                "esessionid": response.cookies['esessionid'],
                "base64": "data:image/png;base64," + image_base64
            }
        except Exception as e:
            print("Imgae_Error:", e.args)
            return {
                "code": "-1",
                "msg": e.args
            }

    def get_score(self, capcha, cookies, esessionid):
        headers = {
            'Connection': 'keep - alive',
            'Host': 'search.neea.edu.cn',
            "Content-Type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            "Referer": "http://search.neea.edu.cn/QueryMarkUpAction.do?act = doQueryCond&pram =results&community=Home&sid=2nasVMoohJ6cFnsQEIjGYmh"
        }
        query_url = "http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryNtceResultsList"
        params = {
            "pram": "results",
            "ksxm": "2nasVMoohJ6cFnsQEIjGYmh",
            "nexturl": "/QueryMarkUpAction.do?act=doQueryCond&sid=2nasVMoohJ6cFnsQEIjGYmh&pram=results&zjhm=" + self.id_num + "&xm=" + self.name,
            "xm": self.name,
            "zjhm": self.id_num,
            "verify": capcha
        }
        # params = urlencode(params)
        response = requests.post(query_url, data=params, headers=headers,
                                 cookies={"verify": cookies, "esessionid": esessionid})
        if '抱歉' in response.text:
            e = re.compile("('.*?')").findall(response.text)[2].replace("'","")
            return {
                "code": "-1",
                "msg": e
            }
        else:
            bs = BeautifulSoup(response.text, 'html.parser')
            table = bs.find_all('table')
            tr = table[3].find_all('tr')
            jsons = []
            for i in tr:
                td = i.find_all('td')
                if not td: continue
                temp = {
                    "object": td[0].text,
                    "score": td[1].text,
                    "ispass": td[2].text,
                    "id_num": td[3].text,
                    "date": td[4].text,
                    "validity": td[5].text,
                    "province": td[6].text
                }
                jsons.append(temp)
            return jsons

    def __init__(self, id_num, name):
        self.name = name
        self.id_num = id_num
