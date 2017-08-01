# -*- coding: utf-8 -*-
import argparse
import json
import os
import requests
import time


VK_TOKEN = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'


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
    API_VER = '5.67'
    DEF_TIME_OUT = 0.5
    user_id = ''
    access_token = ''
    group_tolerance = 0
    output_file = ''
    groups_info_result = []
    user_uniq_groups = {}

    def __init__(self, auth_token, user_id=None, user_name=None, group_tolerance=0, out_file='outGroups.json'):
        self.group_tolerance = group_tolerance
        self.access_token = auth_token
        self.output_file = out_file
        if user_id is None:
            self.get_user_id_by_name(user_name)
        else:
            self.user_id = user_id

    def get_user_id_by_name(self, user_name):
        request_parametrs = {
            'user_ids': user_name,
            'access_token': self.access_token,
            'v': self.API_VER
        }
        vk_response = requests.get('/'.join([self.BASE_URL, self.USER_GET]), request_parametrs)
        self.user_id = vk_response.json()['response'][0]['id']

    def get_friend_list(self):
        request_parametrs = {
            'client_id': self.user_id,
            'access_token': self.access_token,
            'v': self.API_VER,
            # 'count': 3
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

    def get_user_groups(self, req_user):
        request_parametrs = {
            'user_id': req_user,
            'count': 1000,
            'access_token': self.access_token,
            'v': self.API_VER
        }
        timeout = self.DEF_TIME_OUT
        continue_request = True
        in_groups = {-1}
        while continue_request:
            try:
                vk_response = requests.get('/'.join([self.BASE_URL, self.GROUPS_GET]), request_parametrs)
                if 'error' in vk_response.json():
                    if vk_response.json()['error']['error_code'] == 18:
                        continue_request = False
                        continue
                    elif vk_response.json()['error']['error_code'] == 6:
                        time.sleep(timeout)
                        timeout *= 1.1
                        continue
                    elif vk_response.json()['error']['error_code'] == 5:
                        print('Authentification error. Exit')
                        continue
                in_groups = set(vk_response.json()['response']['items'])
            except Exception as e:
                print('Wired. \n Error: {} \n User id is: {}. Group status code:{}, response is {}'.format(
                    e, self.user_id, vk_response.status_code, vk_response.json()))
            continue_request = False
        return in_groups

    def prepare_uniq_groups(self):
        friends_list = self.get_friend_list()
        friends_count = len(friends_list)
        uniq_groups = set()
        friends_cntr = 0
        user_groups = self.get_user_groups(self.user_id)
        friends_groups = {}
        for friend in friends_list:
            friends_groups[friend] = self.get_user_groups(friend)
            friends_cntr += 1
            print('Filling friends groups. Friend {} from {} groups'.format(friends_cntr, friends_count))
            clear_screen()
        # friends_groups = test_data.td_group_2
        for group in user_groups:
            group_tolerance_cntr = 0
            for friend_id in friends_groups:
                include_group = True
                if group in friends_groups[friend_id]:
                    group_tolerance_cntr += 1
                    if group_tolerance_cntr > self.group_tolerance:
                        include_group = False
                        break
            if include_group:
                uniq_groups.add(group)
        self.user_uniq_groups = uniq_groups

    def get_groups_info(self):
        request_parametrs = {
            'group_ids': self.user_uniq_groups,
            'fields': 'name,members_count',
            'v': self.API_VER
        }
        timeout = self.DEF_TIME_OUT
        continue_request = True
        groups_info = []
        while continue_request:
            try:
                vk_response = requests.get('/'.join([self.BASE_URL, self.GROUPS_INFO]), request_parametrs)
                if 'error' in vk_response.json():
                    if vk_response.json()['error']['error_code'] == 18:
                        continue_request = False
                        continue
                    elif vk_response.json()['error']['error_code'] == 6:
                        time.sleep(timeout)
                        timeout *= 1.1
                        continue
                    elif vk_response.json()['error']['error_code'] == 5:
                        print('Authentification error.')
                        return False
                returned_groups = vk_response.json()['response']
                group_info = {}
                for group in returned_groups:
                    group_info['name'] = group['name']
                    group_info['gid'] = group['id']
                    group_info['members_count'] = group['members_count']
                    groups_info.append(group_info)
            except Exception as e:
                print('Wired. \n Error: {} \n User id is: {}. Group status code:{}, response is {}'.format(
                    e, self.user_id, vk_response.status_code, vk_response.json()))
                time.sleep(timeout)
                timeout *= 1.1
                continue
            continue_request = False
        self.groups_info_result = groups_info

    def write_groups_result(self):
        with open(self.output_file, 'w') as wfile:
            json.dump(fp=wfile, obj=self.groups_info_result, sort_keys=True, indent=4, ensure_ascii=False)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Vk Uniq Groups Finder.', add_help=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', action='store', help='user id')
    group.add_argument('-u', action='store', help='user name')
    # parser.add_argument('-t', dest='g_tolerance', action='store', help='group tolerance')
    # parser.add_argument('-a', dest='user_name', action='store', required=False, help='Auth Token')
    parser.add_argument('-o', dest='out_file', action='store', default='outGroups.json', help='OutputFile')
    args = parser.parse_args()
    return vars(args)

if __name__ == '__main__':
    start_arguments = parse_arguments()
    if start_arguments['i'] is None:
        uniq_group = VkUniqGroupFinder(VK_TOKEN, user_name=start_arguments['u'], out_file=start_arguments['out_file'])
    else:
        uniq_group = VkUniqGroupFinder(VK_TOKEN, user_id=start_arguments['i'], out_file=start_arguments['out_file'])
    uniq_group.prepare_uniq_groups()
    uniq_group.get_groups_info()
    uniq_group.write_groups_result()
