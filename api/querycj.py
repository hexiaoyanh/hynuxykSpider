import re
from time import sleep

import requests

from bs4 import BeautifulSoup
import math


class querycj():
    flag = 0

    ############################################查询成绩1 begin#######################################
    def querycj1(self, date):
        payload = {
            'kcmc': '',
            'kcxz': '',
            'kksj': date,
            'ok': '',
            'xsfs': 'qbcj'
        }
        if self.nanyue is True:
            url = "http://59.51.24.41/xszqcjglAction.do?method=queryxscj"
        else:
            url = "http://59.51.24.46/hysf/xszqcjglAction.do?method=queryxscj"
        data = requests.post(url=url, cookies=self.cookie, data=payload)
        soup = BeautifulSoup(data.text, 'html.parser')

        many = int(soup.find(id='PageNavigation').font.text)
        many = math.ceil(many / 10)
        return {
            'toatalPage': many,
            'soup': soup
        }

    ############################################查询成绩1 end#######################################

    ############################################查询成绩2 begin#####################################
    def setjson(self, soup, PageNum):
        where1 = soup.find('input', {'name': 'where1'})['value']
        where2 = soup.find('input', {'name': 'where2'})['value']
        OrderBy = soup.find('input', {'name': 'OrderBy'})['value']
        keyCode = soup.find('input', {'name': 'keyCode'})['value']
        isOutJoin = soup.find('input', {'name': 'isOutJoin'})['value']
        oldSelectRow = soup.find('input', {'name': 'oldSelectRow'})['value']
        printHQL = soup.find('input', {'name': 'printHQL'})['value']
        sqlString = soup.find('input', {'name': 'sqlString'})['value']
        sqlArgs = soup.find('input', {'name': 'sqlArgs'})['value']
        isSql = soup.find('input', {'name': 'isSql'})['value']
        beanName = soup.find('input', {'name': 'beanName'})['value']
        printPageSize = soup.find('input', {'name': 'printPageSize'})['value']
        key = soup.find('input', {'name': 'key'})['value']
        field = soup.find('input', {'name': 'field'})['value']
        totalPages = soup.find('input', {'name': 'totalPages'})['value']
        ZdSzCode = ''
        ZdSzCodeValue = ''
        ZdSzValueTemp = ''
        ZDSXkeydm = ''
        PlAction = ''

        return {
            'where1': where1,
            'where2': where2,
            'OrderBy': OrderBy,
            'keyCode': keyCode,
            'isOutJoin': isOutJoin,
            'PageNum': str(PageNum),
            'oldSelectRow': oldSelectRow,
            'printHQL': printHQL,
            'sqlString': sqlString,
            'sqlArgs': sqlArgs,
            'isSql': isSql,
            'beanName': beanName,
            'printPageSize': printPageSize,
            'key': key,
            'field': field,
            'totalPages': totalPages,
            'ZdSzCode': ZdSzCode,
            'ZdSzCodeValue': ZdSzCodeValue,
            'ZdSzValueTemp': ZdSzValueTemp,
            'ZDSXkeydm': ZDSXkeydm,
            'PlAction': PlAction
        }

    def querycj2(self, soup, PageNum):
        if self.nanyue is True:
            url = "http://59.51.24.41/xszqcjglAction.do?method=queryxscj"
        else:
            url = "http://59.51.24.46/hysf/xszqcjglAction.do?method=queryxscj"
        json = self.setjson(soup, PageNum)
        data = requests.post(url=url, cookies=self.cookie, data=json)
        data = re.search('window\.parent\.document\.getElementById\(\'mxhDiv\'\)\.innerHTML = [\s\S]*?<\/table>',
                         data.text).group()[61:]
        data = data.replace('\\', ' ')
        # data = "<html>" + data
        # data = data + "</html>"
        soup = BeautifulSoup(data, 'html.parser')
        return self.dealsoup(soup)

    ############################################查询成绩2 end#######################################

    def dealsoup(self, soup):
        try:
            table = soup.find(id='mxh')
        except:
            table = soup
        tr = table.find_all('tr')
        json = {}
        for i in tr:
            td = i.find_all('td')
            if td[5].a is None:
                garde = 0
                gradeDetail = ""
            else:
                garde = td[5].a.text
                gradeDetail = td[5].a['onclick']
            try:
                temp = {
                    'id': str(int(td[0].text)),  # 序号
                    'studentID': td[1].text,  # 学号
                    'name': td[2].text,  # 姓名
                    'beginDate': td[3].text,  # 开始日期
                    'className': td[4].text,  # 课程名
                    'grade': garde,  # 成绩
                    'gradeDetail': gradeDetail,  # 成绩详情地址td[5].a['onclick']
                    'gradeFlag': td[6].text,  # 成绩标志
                    'courseNature': td[7].text,  # 课程性质
                    'courseCategory': td[8].text,  # 课程类别
                    'classHour': td[9].text,  # 学时
                    'classgrade': td[10].text,  # 学分
                    'examinationNature': td[11].text,  # 考试性质
                    'other': td[12].text  # 补重学期
                }
            except IndexError:
                temp = {
                    'id': str(int(td[0].text)),  # 序号
                    'studentID': td[1].text,  # 学号
                    'name': td[2].text,  # 姓名
                    'beginDate': td[3].text,  # 开始日期
                    'className': td[4].text,  # 课程名
                    'grade': td[5].a.text,  # 成绩
                    'gradeDetail': td[5].a['onclick'],  # 成绩详情地址td[5].a['onclick']
                    'gradeFlag': td[6].text,  # 成绩标志
                    'courseNature': td[7].text,  # 课程性质
                    'courseCategory': td[8].text,  # 课程类别
                    'classHour': td[9].text,  # 学时
                    'classgrade': td[10].text,  # 学分
                    'examinationNature': td[11].text,  # 考试性质
                    'other': ""  # 补重学期
                }
            json[str(self.flag)] = temp
            self.flag += 1
        return json

    def queryallcj(self, date):
        self.flag = 0
        try:
            json = self.querycj1(date)
        except AttributeError:
            return {
                "code": -1,
                "msg": "服务器错误"
            }
        data = self.dealsoup(json['soup'])
        for i in range(1, json['toatalPage']):
            temp = self.querycj2(json['soup'], i + 1)
            data = dict(data, **temp)
        return data

    def __init__(self, cookie, nanyue):
        self.cookie = {'JSESSIONID': cookie}
        self.nanyue = nanyue
