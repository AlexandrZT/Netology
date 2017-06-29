# -*-coding: utf-8 -*-
import requests
import urllib

def create_url(app_id):
    URL = 'https://oauth.yandex.ru/authorize'
    url_parametrs = {
        'response_type' : 'token',
        'client_id' : app_id
        }
    return '?'.join((URL, urllib.parse.urlencode(url_parametrs)))

class YaBase():
    API_KEY = ''
    API_PASSWORD = ''

    def __init__(self, api_key, api_password):
        self.API_KEY = api_key
        self.API_PASSWORD = api_password




class YaCounters(YaBase):
    pass

print(create_url(''))