"""
@File : cet.py
@Author: Mika
@Date : 2020/2/21
@Desc :
"""
import requests
import re
import random
from PIL import Image
from urllib.parse import urlencode


def get_info():
    id_num = input("输入准考证号：")
    name = input("输入姓名：")
    level = id_num[9]
    return id_num, name, level


def get_img(Session, id_numm):
    try:
        headers = {
            'Connection': 'keep - alive',
            'Host': 'cache.neea.edu.cn',
            'Referer': 'http://cet.neea.edu.cn/cet',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36',
        }
        Session.headers = headers
        get_url = 'http://cache.neea.edu.cn/Imgs.do?'
        params = {
            'c': 'CET',
            'ik': id_numm,
            't': random.random()
        }
        response = Session.get(get_url, params=params)
        img_url = re.compile('"(.*?)"').findall(response.text)[0]
        img_url = "http://cet.neea.edu.cn/imgs/" + img_url + ".png"
        print(img_url)
        img = requests.get(img_url, timeout=None)
        with open("/Users/mika/img.png", 'wb') as f:
            f.write(img.content)
        Image.open("/Users/mika/img.png").show()
    except Exception as e:
        print("Imgae_Error:", e.args)


def get_score(Session, id_num, name, level):
    capcha = input('请打开图片输入验证码:')
    print(capcha)
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
        'data': test.get(level) + ',' + id_num + ',' + name,
        'v': capcha
    }
    data = urlencode(data)
    print(data)
    response = Session.get(query_url, params=data, headers=headers)
    print(response.text)
    if 'error' in response.text:
        e = re.compile("'error':'(.*?)'|error:'(.*?)'").findall(response.text)[0]
        if e is not None:
            # print(e)
            if '验证码错误' in e[1]:
                print("验证码输入错误！")
                get_img(Session, id_num)
                get_score(Session, id_num, name)
            else:
                print(e[0])
    else:
        id_num = re.compile("z:'(.*?)'").findall(response.text)[0]
        name = re.compile("n:'(.*?)'").findall(response.text)[0]
        school = re.compile("x:'(.*?)'").findall(response.text)[0]
        score = re.compile("s:(.*?),").findall(response.text)[0]
        listening = re.compile("l:(.*?),").findall(response.text)[0]
        reading = re.compile("r:(.*?),").findall(response.text)[0]
        writing = re.compile("w:(.*?),").findall(response.text)[0]
        rank = re.compile("kys:'(.*?)'").findall(response.text)[0]
        if level == '1':
            print("\n====================\n\n四级笔试成绩：")
        elif level == '2':
            print("\n====================\n\n六级笔试成绩：")
        print("准考证号：" + str(id_num))
        print("姓名：" + str(name))
        print("学校：" + str(school))
        print("总分：" + str(score))
        print("听力：" + str(listening))
        print("阅读：" + str(reading))
        print("写作与翻译：" + str(writing))
        if level == '1':
            print("\n====================\n\n四级口试成绩：")
        elif level == '2':
            print("\n====================\n\n六级口试成绩：")
        print("等级：" + str(rank))


def main():
    id_num, name, level = get_info()
    s = requests.Session()
    get_img(s, id_num)
    get_score(s, id_num, name, level)
    end = input("输入任意键退出...")


if __name__ == '__main__':
    main()
