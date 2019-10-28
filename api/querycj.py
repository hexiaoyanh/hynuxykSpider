import re

import requests

from .login import login
from bs4 import BeautifulSoup
import math


class querycj(login):
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

        url = "http://59.51.24.46/hysf/xszqcjglAction.do?method=queryxscj"
        data = requests.post(url=url, cookies=self.cookie, data=payload)
        soup = BeautifulSoup(data.text, 'html.parser')
        try:
            many = int(soup.find(id='PageNavigation').font.text)
            many = math.ceil(many / 10)
        except AttributeError:
            raise EnvironmentError
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
        flag = 0
        for i in tr:
            td = i.find_all('td')
            temp = {
                'id': str(int(td[0].text)),  # 序号
                'studentID': td[1].text,  # 学号
                'name': td[2].text,  # 姓名
                'beginDate': td[3].text,  # 开始日期
                'className': td[4].text,  # 课程名
                'grade': td[5].a.text,  # 成绩
                'gradeDetail': td[5].a['onclick'],  # 成绩详情地址
                'gradeFlag': td[6].text,  # 成绩标志
                'courseNature': td[7].text,  # 课程性质
                'courseCategory': td[8].text,  # 课程类别
                'classHour': td[9].text,  # 学时
                'classgrade': td[10].text,  # 学分
                'examinationNature': td[11].text,  # 考试性质
                'other': td[12].text  # 补重学期
            }
            json[str(self.flag)] = temp
            self.flag += 1
        return json

    def queryallcj(self, date):
        self.flag = 0
        json = self.querycj1(date)
        data = self.dealsoup(json['soup'])
        for i in range(1, json['toatalPage']):
            temp = self.querycj2(json['soup'], i + 1)
            data = dict(data, **temp)
        return data

    def __init__(self, *args):
        if len(args) == 2:
            super().__init__(str(args[0]), str(args[1]))
        else:
            self.cookie = {'JSESSIONID': args[0]}
