# -*-coding: utf-8 -*-
import requests
import urllib


def create_url(app_id):
    url = 'https://oauth.yandex.ru/authorize'
    url_parametrs = {
        'response_type': 'token',
        'client_id': app_id
        }
    return '?'.join((url, urllib.parse.urlencode(url_parametrs)))


class YaBase():
    API_KEY = ''
    API_TOKEN = ''
    BASE_URL = 'https://api-metrika.yandex.ru/management/v1'

    def __init__(self, api_key, api_token):
        self.API_KEY = api_key
        self.API_TOKEN = api_token

    def prepare_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.API_TOKEN),
            'Content-Type': 'application/json'
        }

    def check_run(self):
        if self.API_KEY and self.API_TOKEN:
            return True
        else:
            return False


class YaCounters(YaBase):
    COUNTERS_URL = 'counters'
    COUNTERS_STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/data'
    cntr_id = 0

    def get_counter_id(self):
        if not self.check_run():
            return False
        response = requests.get('/'.join((self.BASE_URL, self.COUNTERS_URL)), headers=self.prepare_headers())
        self.cntr_id = response.json()['counters'][0]['id']
        return True

    def get_visitors(self):
        req_params = {
                'id': self.cntr_id,
                'metrics': 'ym:s:visits'
        }
        if not self.cntr_id:
            self.get_counter_id()
        req_headers = self.prepare_headers()
        response = requests.get(self.COUNTERS_STAT_URL, params=req_params, headers=req_headers)
        return response.json()['totals'][0]

yam = YaCounters('ID', 'TOKEN')
yam_cntrs = yam.get_counter_id()
yam_number = yam.get_visitors()
print(yam_number)
