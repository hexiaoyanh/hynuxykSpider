import json

from api.querycj import querycj


class api:

    def querycj(self, date):
        jsons = self.querygrade.queryallcj(date)
        return json.dumps(jsons, ensure_ascii=False)

    def __init__(self, username, password):
        self.querygrade = querycj(username, password)
