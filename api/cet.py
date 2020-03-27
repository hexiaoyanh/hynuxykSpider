"""
@File : cet.py
@Author: Mika
@Date : 2020/2/21
@Desc :
"""
import base64

import requests
import re
import random
from PIL import Image
from urllib.parse import urlencode


class cet:

    def get_img(self):
        try:
            headers = {
                'Connection': 'keep - alive',
                'Host': 'cache.neea.edu.cn',
                'Referer': 'http://cet.neea.edu.cn/cet',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36',
            }
            get_url = 'http://cache.neea.edu.cn/Imgs.do?'
            params = {
                'c': 'CET',
                'ik': self.id_num,
                't': random.random()
            }
            response = requests.get(get_url, params=params, headers=headers)
            img_url = re.compile('"(.*?)"').findall(response.text)[0]

            img_url = "http://cet.neea.edu.cn/imgs/" + img_url + ".png"
            img = requests.get(img_url, timeout=None, cookies=response.cookies)
            image_base64 = str(base64.b64encode(img.content), encoding='utf-8')
            return {
                "code": "1",
                "cookies": response.cookies['verify'],
                "base64": "data:image/png;base64," + image_base64
            }
        except Exception as e:
            print("Imgae_Error:", e.args)
            return {
                "code": "-1",
                "msg": e.args
            }

    def get_score(self, capcha, cookies):
        headers = {
            'Connection': 'keep - alive',
            'Host': 'cache.neea.edu.cn',
            'Origin': 'http://cet.neea.edu.cn',
            'Referer': 'http://cet.neea.edu.cn/cet',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36',
        }

        query_url = "http://cache.neea.edu.cn/cet/query"

        test = {
            '1': 'CET4_192_DANGCI',
            '2': 'CET6_192_DANGCI',
        }
        data = {
            'data': test.get(self.level) + ',' + self.id_num + ',' + self.name,
            'v': capcha
        }
        data = urlencode(data)
        response = requests.get(query_url, params=data, headers=headers, cookies={"verify": cookies})
        if 'error' in response.text:
            e = re.compile("'error':'(.*?)'|error:'(.*?)'").findall(response.text)[0]
            if e is not None:
                if '验证码错误' in e[1]:
                    return {
                        "code": "-1",
                        "msg": e[1]
                    }
                else:
                    return {
                        "code": "-1",
                        "msg": e[0]
                    }
        else:
            id_num = re.compile("z:'(.*?)'").findall(response.text)[0]
            name = re.compile("n:'(.*?)'").findall(response.text)[0]
            school = re.compile("x:'(.*?)'").findall(response.text)[0]
            score = re.compile("s:(.*?),").findall(response.text)[0]
            listening = re.compile("l:(.*?),").findall(response.text)[0]
            reading = re.compile("r:(.*?),").findall(response.text)[0]
            writing = re.compile("w:(.*?),").findall(response.text)[0]
            rank = re.compile("kys:'(.*?)'").findall(response.text)[0]
            jsons = {
                "id_num": str(id_num),
                "name": str(name),
                "school": str(school),
                "score": str(score),
                "listending": str(listening),
                "reading": str(reading),
                "writing": str(writing),
                "rank": str(rank)
            }
            return jsons

    def __init__(self, id_num, name):
        self.id_num = id_num
        self.name = name
        self.level = id_num[9]
