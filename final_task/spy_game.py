# -*- coding: utf-8 -*-
import requests
from urllib.parse import urlencode
import time

BASE_URL = 'https://api.vk.com/method'
FRIENDS_GET = 'friends.get'
GROUPS_GET = 'groups.get'
USER_GET = 'users.get'
APP_ID = 6075011
API_VER = '5.67'
DEF_TIME_OUT = 0.5
VK_TOKEN = 'd13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22'


def get_friend_list(user_id, access_token):
    request_parametrs = {
                        'client_id': user_id,
                        'access_token': access_token,
                        'v': API_VER
    }
    timeout = DEF_TIME_OUT
    continue_request = True
    friends_list = []
    while continue_request:
        try:
            vk_response = requests.get('/'.join([BASE_URL, FRIENDS_GET]), request_parametrs)
            friends_list = vk_response.json()['response']['items']
        except:
            time.sleep(timeout)
            timeout *= 1.1
            continue
        continue_request = False
    return friends_list


def get_user_groups(user_id, access_token):
    request_parametrs = {
                        'client_id': user_id,
                        'access_token': access_token,
                        'v': API_VER
    }
    timeout = DEF_TIME_OUT
    continue_request = True
    while continue_request:
        try:
            vk_response = requests.get('/'.join([BASE_URL, GROUPS_GET]), request_parametrs)
            print(vk_response.json())
            in_groups = vk_response.json()['response']['items']
        except:
            time.sleep(timeout)
            timeout *= 1.1
            continue
        continue_request = False
    return in_groups

# friends_list = get_friend_list(5030613, VK_TOKEN, wrk_time_out)
# friends_list = get_friend_list(5030613, VK_TOKEN)
id_groups = get_user_groups(5030613, VK_TOKEN)