"""
@File : elective.py
@Author: Mika
@Date : 2020/3/27
@Desc :
"""
import requests,re
from bs4 import BeautifulSoup


class elective:

    def getXklb(self):
        if self.nanyue is True:
            url = "http://59.51.24.41/xkglAction.do?method=xsxkXsxk"
        else:
            url = "http://59.51.24.46/hysf/xkglAction.do?method=xsxkXsxk"
        data = requests.get(url, cookies=self.cookie, timeout=15)
        bs = BeautifulSoup(data.text, 'html.parser')
        try:
            table = bs.find(id='mxh')
        except:
            return {"Code": "-1", "Msg": "当前没有选课"}
        tr = table.find_all('tr')
        json = []
        for i in tr:
            td = i.find_all('td')
            temp = {
                'id': str(int(td[0].text)),  # 序号
                'date': td[1].text,  # 日期
                'electiveCategory': td[2].text,  # 选课类型
                'electiveStage': td[3].text,  # 选课阶段
                'electiveStarttime': td[4].text,  # 选课开始阶段,
                'electiveEndtime': td[5].text,  # 选课结束时间
                'onclick': td[6].a['onclick']
            }
            json.append(temp)
        return json

    def getallcourse(self, data):
        if self.nanyue is True:
            url = "http://59.51.24.41/xkglAction.do?method=toFindxskxkclb&xnxq01id="+data+"&zzdxklbname=1&type=1&jx02kczid=null"
        else:
            url = "http://59.51.24.46/hysf/xkglAction.do?method=toFindxskxkclb&xnxq01id="+data+"&zzdxklbname=1&type=1&jx02kczid=null"
        data = requests.get(url,cookies=self.cookie, timeout=15)
        bs = BeautifulSoup(data.text, 'html.parser')
        try:
            table = bs.find(id='mxh')
        except:
            return {"Code": "-1", "Msg": "当前没有选课"}
        tr = table.find_all('tr')
        json = []
        for i in tr:
            td = i.find_all('td')
            temp = {
                'id': str(int(td[0].text)),  # 序号
                'courseName': td[1].text.replace('\xa0', ''),  # 课程名
                'startUnit': td[2].text.replace('\xa0', ''),  # 开课单位
                'credit': td[3].text.replace('\xa0', ''),  # 学分
                'capacity': td[4].text.replace('\xa0', ''),  # 容量,
                'margin': td[5].text.replace('\xa0', ''),  # 余量
                'teacher': td[6].a.text.replace('\xa0', ''), #老师
                'weekOfclass':td[7].text.replace('\xa0', ''),#上课周次
                'classTime':td[8].text.replace('\xa0', ''),#上课时间
                'classLocations':td[9].text.replace('\xa0', ''),#上课地点
                'courseAttributes':td[10].text.replace('\xa0', ''),#课程性质
                'groupName':td[11].text.replace('\xa0', ''),#分组名
                'genderRequirements':td[12].text.replace('\xa0', ''),#性别要求
                'class':td[13].text.replace('\xa0', ''),#上课班级
                'onclick':td[14].a['onclick']
            }
            json.append(temp)
        return json

    def pickcourse(self,url):
        if self.nanyue is True:
            urls = "http://59.51.24.41" + re.search("'.*'", url).group(0).replace("'", "")
        else:
            urls = "http://59.51.24.46" + re.search("'.*'", url).group(0).replace("'", "")
        data = requests.get(urls,cookies=self.cookie, timeout=15)
        msg = re.search("'.*'", data.text[35:]).group(0).replace("'", "")
        return msg


    def __init__(self, cookie, nanyue):
        self.cookie = {'JSESSIONID': cookie}
        self.nanyue = nanyue
