# 衡阳师范学院教务网站爬虫（强智教务网站）

## 使用方法

### 查询成绩
```python
import api 
a = api('Usernme','Password')
a.querycj('Date(2018-2019-2)')
```

## 查询课表
```python
a = api('Username','Password')
a.querykb('Date(2018-2019-2)','Week(1)')
```