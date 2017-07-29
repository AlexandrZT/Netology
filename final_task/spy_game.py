# -*- coding: utf-8 -*-
import os
import requests
from urllib.parse import urlencode
import time
import test_data


def clear_screen():
    if os.name in ('nt', 'dos'):
        os.system('cls')
    elif os.name in ('linux', 'osx', 'posix'):
        os.call("clear")


class VkUniqGroupFinder:
    BASE_URL = 'https://api.vk.com/method'
    FRIENDS_GET = 'friends.get'
    GROUPS_GET = 'groups.get'
    GROUPS_INFO = 'groups.getById'
    USER_GET = 'users.get'
    APP_ID = 6075011
    API_VER = '5.67'
    DEF_TIME_OUT = 0.5
    VK_TOKEN = 'd13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22'
    user_id = ''
    access_token = ''
    group_tolerance = 0

    def __init__(self, auth_token, user_id=None, user_name=None, group_tolerance=0):
        self.group_tolerance = group_tolerance
        self.access_token = auth_token
        if user_id is None:
            self.user_id = self.get_user_id_by_name(user_name)
        else:
            self.user_id = user_id

    def get_user_id_by_name(self, user_name):
        pass

    def get_friend_list(self):
        request_parametrs = {
            'client_id': self.user_id,
            'access_token': self.access_token,
            'v': self.API_VER,
            'count': 3
        }
        timeout = self.DEF_TIME_OUT
        continue_request = True
        friends_list = []
        while continue_request:
            try:
                vk_response = requests.get('/'.join([self.BASE_URL, self.FRIENDS_GET]), request_parametrs)
                friends_list = vk_response.json()['response']['items']
            except:
                time.sleep(timeout)
                timeout *= 1.1
                continue
            continue_request = False
        return friends_list

    def get_user_groups(self):
        request_parametrs = {
            'user_id': self.user_id,
            'count': 1000,
            'access_token': self.access_token,
            'v': self.API_VER
        }
        timeout = self.DEF_TIME_OUT
        continue_request = True
        while continue_request:
            try:
                vk_response = requests.get('/'.join([self.BASE_URL, self.GROUPS_GET]), request_parametrs)
                if 'error' in vk_response.json():
                    if vk_response.json()['error']['error_code'] == 18:
                        continue_request = False
                        in_groups = set([-1, ])
                        continue
                    elif vk_response.json()['error']['error_code'] == 6:
                        time.sleep(timeout)
                        timeout *= 1.1
                        continue
                in_groups = set(vk_response.json()['response']['items'])
            except Exception as e:
                print('Wired. \n Error: {} \n User id is: {}. Group status code:{}, response is {}'.format(
                    e, self.user_id, vk_response.status_code, vk_response.json()))
                time.sleep(timeout)
                timeout *= 1.1
                continue
            continue_request = False
        return in_groups

    def return_uniq_groups(self):
        friends_list = self.get_friend_list()
        friends_count = len(friends_list)
        uniq_groups = set()
        friends_cntr = 0

        print('Got user with {} friends'.format(friends_count))
        # user_groups = get_user_groups(user_id, access_token)
        user_groups = test_data.tdatas_user_2
        print(user_groups)
        friends_groups = {}
        # for friend in friends_list:
        #     print(friend)
        #     friends_groups[friend] = get_user_groups(friend, access_token)
        #     friends_cntr += 1
        #     clear_screen()
        #     print('Current friend is {} from {}'.format(friends_cntr, friends_count))
        friends_groups = test_data.td_group_2
        for group in user_groups:
            print('Working with group: {}'.format(group))
            group_tolerance_cntr = 0
            for friend_id in friends_groups:
                print('Current groups:', friends_groups[friend_id])
                include_group = True
                if group in friends_groups[friend_id]:
                    print('Group id {} is in friend id: {} groups'.format(group, friend_id))
                    group_tolerance_cntr += 1
                    if group_tolerance_cntr > self.group_tolerance:
                        print('Group id {} excluded'.format(group))
                        include_group = False
                        break
            if include_group:
                uniq_groups.add(group)
                print('Group id {} is uniq, length:{}'.format(group, len(uniq_groups)))
        return uniq_groups

    def get_groups_info(self, selected_groups):
        request_parametrs = {
            'group_ids': selected_groups,
            'fields': 'name,description, members_count',
            'v': self.API_VER
        }
        vk_response = requests.get('/'.join([self.BASE_URL, self.GROUPS_INFO]), request_parametrs)

    def write_groups_result(self, file_to_write):
        pass




groups = return_uniq_groups(5030613, VK_TOKEN, 1)
print(groups)
