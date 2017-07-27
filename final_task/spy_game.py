# -*- coding: utf-8 -*-
import os
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
                        # 'count': 3
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
                        'user_id': user_id,
                        'access_token': access_token,
                        'v': API_VER
    }
    timeout = DEF_TIME_OUT
    continue_request = True
    while continue_request:
        try:
            vk_response = requests.get('/'.join([BASE_URL, GROUPS_GET]), request_parametrs)
            # print('User id is: {}. Group status code:{}, response is {}'.format(user_id, vk_response.status_code, vk_response.json()))
            if 'error' in vk_response.json():
                if vk_response.json()['error']['error_code'] == 18:
                    continue_request = False
                    in_groups = set([-1,])
                    continue
                elif vk_response.json()['error']['error_code'] == 6:
                    time.sleep(timeout)
                    timeout *= 1.1
                    continue
            in_groups = set(vk_response.json()['response']['items'])
        except Exception as e:
            print(e, vk_response.status_code)
            print('User id is: {}. Group status code:{}, response is {}'.format(user_id, vk_response.status_code,
                                                                                vk_response.json()))
            time.sleep(timeout)
            timeout *= 1.1
            continue
        continue_request = False
    return in_groups


def return_uniq_groups(user_id, access_token, group_tolerance):
    friends_list = get_friend_list(user_id, access_token)
    friends_count = len(friends_list)
    friends_cntr = 0
    group_tolerance_cntr = 0
    print('Got user with {} friends'.format(friends_count))
    user_groups = get_user_groups(user_id, access_token)
    friends_groups = {}
    for friend in friends_list:
        print(friend)
        friends_groups[friend] = get_user_groups(friend, access_token)
        friends_cntr += 1
        os.system('cls')
        print('Current friend is {} from {}'.format(friends_cntr, friends_count))
    for group in user_groups:
        for friend_id in friends_groups:
            print(group, friends_groups[friend_id])
            if group in friends_groups[friend_id]:
                print('Group id {} is in friend id: {} groups'.format(group, friend_id))
                group_tolerance_cntr += 1
                if group_tolerance_cntr > group_tolerance:
                    print('Group id {} excluded'.format(group))
                    break
        print('Group id {} is uniq'.format(group))

    return friends_groups


groups = return_uniq_groups(5030613, VK_TOKEN, 0)
