import json

from .querycj import querycj
from .querykb import querykb


class api:
    cookie = None

    def querycj(self, date):
        jsons = self.querygrade.queryallcj(date)
        return json.dumps(jsons, ensure_ascii=False)

    def querykb(self, date, week):
        return self.querykebiao.queryallkb(date, week)

    def getcookie(self):
        return self.cookie

    def __init__(self, *args):
        if len(args) == 2:
            self.querygrade = querycj(args[0], args[1])
            self.cookie = self.querygrade.cookie
            self.querykebiao = querykb(self.cookie)
        else:
            self.querygrade = querycj(args[0])
            self.querykebiao = querykb(args[0])
            self.cookie = {'JSESSIONID': args[0]}

