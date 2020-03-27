"""
@File : ncre.py
@Author: Mika
@Date : 2020/3/27
@Desc :
"""
import base64
import json
import random
import re

import requests
from bs4 import BeautifulSoup


class ncre:
    def get_data(self):
        try:
            headers = {
                'Connection': 'keep - alive',
                'Host': 'search.neea.edu.cn',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            }
            get_url = "http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryCond&pram=results&community=Home&sid=300"
            response = requests.get(get_url, headers=headers)
            date = []
            bs = BeautifulSoup(response.text, 'html.parser')
            ksnf = bs.find('select', {'name': 'ksnf'})
            option = ksnf.find_all('option')
            for i in option:
                temp = {
                    "value": i['value'],
                    "date": i.text
                }
                date.append(temp)
            types = []
            type_url = "http://search.neea.edu.cn/QueryDataAction.do?act=doQuerySfBkjb&examid=3USNkTYIJ7H94M1zXwUBnV3"
            data = requests.get(type_url, headers=headers)
            bkjb = json.loads(data.text)

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
                "base64": "data:image/png;base64," + image_base64,
                "date": date,
                "type": bkjb
            }
        except Exception as e:
            print("Imgae_Error:", e.args)
            return {
                "code": "-1",
                "msg": e.args
            }

    def get_socre(self, capcha, verify, esessionid, ksnf, bkjb):
        headers = {
            'Connection': 'keep - alive',
            'Host': 'search.neea.edu.cn',
            "Content-Type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            "Referer": "http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryCond&sid=300&pram=results&psid="
        }
        query_url = "http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryResults"
        params = {
            "pram": "results",
            "ksxm": "300",
            "sf": "",
            "zkzh": "",
            "nexturl": "",
            "ksnf": ksnf,
            "bkjb": bkjb,
            "name": self.name,
            "sfzh": self.id_num,
            "verify": capcha
        }
        # params = urlencode(params)
        response = requests.post(query_url, data=params, headers=headers,
                                 cookies={"verify": verify, "esessionid": esessionid})
        if '抱歉' in response.text:
            e = re.compile("('.*?')").findall(response.text)[2].replace("'", "")
            return {
                "code": "-1",
                "msg": e
            }
        else:
            if "eers" in response.text:
                return {
                    "code": "-1",
                    "msg": "您查询的结果为空，请按以下步骤再次确认：1、	请再次核实所输入信息是否正确。2、	如果您是按身份证件上的信息输入，请查看身份证件与证书上的信息是否相符，若不相符请按成绩单或证书上的姓名、身份证件号码输入。"
                }
            bs = BeautifulSoup(response.text, 'html.parser')
            table = bs.findAll(name="table", attrs={"class": "imgtab"})[0]
            tr = table.find_all('tr')
            head_url = "http://search.neea.edu.cn" + tr[0].find_all('td')[0].find_all('img')[0].get('src')
            headers = {
                'Connection': 'keep - alive',
                'Host': 'search.neea.edu.cn',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                "Referer": "http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryResults"
            }
            img = requests.get(head_url, headers=headers, cookies=response.cookies)
            image_base64 = str(base64.b64encode(img.content), encoding='utf-8')
            data = {
                "head": "data:image/png;base64," + image_base64,
                "name": tr[1].find_all('td')[1].text,
                "id_num": tr[1].find_all('td')[3].text,
                "sfzid": tr[2].find_all('td')[1].text,
                "year": tr[2].find_all('td')[3].text,
                "grade": tr[3].find_all('td')[1].text,
                "month": tr[3].find_all('td')[3].text
            }
            return data

    def __init__(self, id_num, name):
        self.id_num = id_num
        self.name = name
