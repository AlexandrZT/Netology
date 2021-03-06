# -*- coding: utf-8 -*-
import requests
from urllib.parse import urlencode

AUTH_URL = 'https://oauth.vk.com/authorize'
BASE_URL = 'https://api.vk.com/method'
FRIENDS_URL = 'friends.get'
USER_GET = 'users.get'
APP_ID = 6075011
API_VER = '5.67'
protected_key = '<SKIP>'
service_key = '<SKIP>'
access_token = '<SKIP>'


def print_auth_request():
    req_api_params = {
            'client_id': APP_ID,
            'response_type': 'token',
            'scope': 'notify, friends, status, groups',
            'v': API_VER
    }
    print('?'.join([AUTH_URL, urlencode(req_api_params)]))

def get_common_frineds_list():
    request_parametrs = {
                        'client_id': APP_ID,
                        'access_token': access_token,
                        'v': API_VER
    }
    vk_response = requests.get('/'.join([BASE_URL, USER_GET]), request_parametrs)
    my_id = vk_response.json()['response'][0]['id']
    vk_response = requests.get('/'.join([BASE_URL, FRIENDS_URL]), request_parametrs)
    friends_count = vk_response.json()['response']['count']
    friends_list = vk_response.json()['response']['items']
    intersection_list = set(friends_list)
    intersection_list.add(my_id)
    all_friends = []
    print('Получено друзей :', friends_count)
    for friend in friends_list:
        request_parametrs['user_id'] = friend
        vk_response = requests.get('/'.join([BASE_URL, FRIENDS_URL]), request_parametrs)
        if not 'error' in vk_response.json():
            friends_reqested_list = vk_response.json()['response']['items']
        else:
            continue
        all_friends += friends_reqested_list
        intersection_list &= set(friends_reqested_list)
    print('ID Общих друзей:', intersection_list, 'Количество:', len(intersection_list))
    print('Всего круг друзей:', len(all_friends) - len(friends_list))
    for friend in intersection_list:
        request_parametrs['user_id'] = friend
        request_parametrs['fields'] ='first_name, last_name'
        vk_response = requests.get('/'.join([BASE_URL, USER_GET]), request_parametrs)
        print('ID:{} - {} {}'.format(vk_response.json()['response'][0]['id'],vk_response.json()['response'][0]['first_name'],vk_response.json()['response'][0]['last_name']))

def get_common_frineds_list_graph():
    request_parametrs = {
                        'client_id': APP_ID,
                        'access_token': access_token,
                        'v': API_VER
    }
    graph = {}
    vk_response = requests.get('/'.join([BASE_URL, USER_GET]), request_parametrs)
    my_id = vk_response.json()['response'][0]['id']
    vk_response = requests.get('/'.join([BASE_URL, FRIENDS_URL]), request_parametrs)
    friends_count = vk_response.json()['response']['count']
    friends_list = vk_response.json()['response']['items']
    graph[my_id] = friends_list
    print('Получено друзей :', friends_count)
    for friend in friends_list:
        request_parametrs['user_id'] = friend
        vk_response = requests.get('/'.join([BASE_URL, FRIENDS_URL]), request_parametrs)
        if not 'error' in vk_response.json():
            graph[friend] = vk_response.json()['response']['items']
        else:
            print('Banned! id', friend)
    for friend in graph:
        print('{}-{}'.format(friend, graph[friend]))

#get_common_frineds_list()
# get_common_frineds_list_graph()
print_auth_request()