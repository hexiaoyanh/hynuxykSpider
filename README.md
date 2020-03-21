# 衡阳师范学院教务网站爬虫（强智教务网站）

## 使用方法

```python
# 登录获得cookie
from api.jwlogin import jwlogin
logins = jwlogin("username","password",False)#用户名，密码和是否为南岳学院
cookie = logins.login()

# 查询成绩
from api.querycj import querycj
cj = querycj(cookie,False)#登录时所获取的cookie和是否为南岳学院
print(cj.queryallcj("2019-2020-1"))#日期形式为2019-2020-1类似形式

# 查询课表
from api.querykb import querykb
kb = querykb(cookie,False)
print(kb.queryallkb("2019-2020-1","0"))#日期和周数

# 查询平时成绩
from api.queryqxcj import querypscj
print(querypscj(url,cookie,False))#之前查成绩获取的参数url

# 修改密码
from api.findpassword import findpassword
findp = findpassword("username","idcardnum")#学号和身份证号码
print(findp.findpassword())
```