# -*- coding: utf-8 -*-
"""
VK Spy Game (Netology project)
~~~~~~~~~~~~~~~~~~~~~

Spy game is project aimed to find out our differencies in interests between our community
WARNING! VK Key currently is static and should be entered with command line argument
usage:

   >>> ugroups = VkUniqGroupFinder(VK_TOKEN, user_name, out_file)
   >>> ugroups.run()

VK_TOKEN  - uniq access token from Vk API
user_name - Vk UserName or User ID
out_file  - file to write unig groups and some group info

:copyright: (c) 2017 by Alexandr Zaburdyayev.
:license: Apache 2.0, see LICENSE for more details.
"""
import argparse
import json
import os
import requests
import time
import sys


def clear_screen():
    if os.name in ('nt', 'dos'):
        os.system('cls')
    elif os.name in ('linux', 'osx', 'posix'):
        os.system("clear")


def printprogressbar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledlength = int(length * iteration // total)
    bar = fill * filledlength + '-' * (length - filledlength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


class VkUniqGroupFinder:
    user_id = None
    group_tolerance = 0
    output_file = None
    groups_info_result = []
    user_uniq_groups = {}
    BASE_URL = 'https://api.vk.com/method'
    FRIENDS_GET = 'friends.get'
    GROUPS_GET = 'groups.get'
    GROUPS_INFO = 'groups.getById'
    USER_GET = 'users.get'
    PROFILE_INFO = 'account.getProfileInfo'
    API_VER = '5.67'
    DEF_TIME_OUT = 0.5
    access_token = ''
    auth_fail = False
    def_request_parametrs = {
        'access_token': '',
        'v': API_VER
    }

    def __init__(self, auth_token, user_id=None, user_name=None, group_tolerance=0, out_file='outGroups.json'):
        self.group_tolerance = group_tolerance
        self.access_token = auth_token
        self.def_request_parametrs['access_token'] = auth_token
        self.output_file = out_file
        if user_id is None:
            self.get_user_id_by_name(user_name)
        else:
            self.user_id = user_id
        self.check_token()

    def check_token(self,):
        request_parametrs = {
            'access_token': self.access_token,
            'v': self.API_VER
        }
        vk_response = requests.get('/'.join([self.BASE_URL, self.PROFILE_INFO]), request_parametrs).json()
        if 'error' in vk_response:
            print('Auth token incorrect.')
            self.auth_fail = True

    def prepare_parametrs(self, request_params):
        return {**self.def_request_parametrs, **request_params}

    def do_api_request(self, req_url, req_api_params):
        if self.auth_fail:
            return None
        timeout = self.DEF_TIME_OUT
        continue_request = True
        api_return = None
        while continue_request:
            try:
                vk_response = requests.get(req_url, self.prepare_parametrs(req_api_params)).json()
                if 'error' in vk_response:
                    if vk_response['error']['error_code'] == 18:     # Page deleted or blocked
                        continue_request = False
                        continue
                    elif vk_response['error']['error_code'] == 6:    # Too much requests
                        time.sleep(timeout)
                        timeout *= 1.1
                        continue
                    elif vk_response['error']['error_code'] == 7:    # Permission to perform this action is denied
                        continue_request = False
                        continue
                    elif vk_response['error']['error_code'] == 5 or \
                            vk_response['error']['error_code'] == 28:  # Auth failed
                        print('Authentification error. Code: {}.\nExit.'.format(vk_response['error']['error_code']))
                        self.auth_fail = True
                        continue_request = False
                        continue
                api_return = vk_response
            except Exception as e:
                print('Wired. \n Error: {} \n Request parameters: {}. '
                      'Response status code: {},\n api response {}'.format(
                       e, req_api_params, vk_response.status_code, vk_response.json()))
            continue_request = False
        return api_return

    def get_user_id_by_name(self, user_name):
        request_parametrs = {
            'user_ids': user_name,
        }
        vk_response = self.do_api_request('/'.join([self.BASE_URL, self.USER_GET]), request_parametrs)
        self.user_id = vk_response['response'][0]['id']

    def get_friends_list(self, req_user_id):
        request_parametrs = {
            'user_id': req_user_id,
            # 'count': 3    # DEBUG Limitter
        }
        vk_response = self.do_api_request('/'.join([self.BASE_URL, self.FRIENDS_GET]), request_parametrs)
        if self.auth_fail:
            return
        friends_list = vk_response['response']['items']
        return friends_list

    def get_user_groups(self, req_user):
        request_parametrs = {
            'user_id': req_user,
            'count': 1000,
        }
        if self.auth_fail:
            return
        vk_response = self.do_api_request('/'.join([self.BASE_URL, self.GROUPS_GET]), request_parametrs)
        if vk_response is None:
            in_groups = {-1}
        else:
            in_groups = set(vk_response['response']['items'])
        return in_groups

    def get_groups_info(self):
        request_parametrs = {
            'group_ids': str(self.user_uniq_groups).strip('{}'),
            'fields': 'name,members_count',
        }
        if self.auth_fail:
            return
        groups_info = []
        vk_response = self.do_api_request('/'.join([self.BASE_URL, self.GROUPS_INFO]), request_parametrs)
        returned_groups = vk_response['response']
        for group in returned_groups:
            if 'deactivated' in group:
                groups_info.append({'gid': group['id'], 'name': group['name'], 'members_count': 'BANNED'})
            else:
                groups_info.append({'gid': group['id'], 'name': group['name'], 'members_count': group['members_count']})
        self.groups_info_result = groups_info

    def prepare_uniq_groups(self):
        friends_list = self.get_friends_list(self.user_id)
        if self.auth_fail:
            return
        friends_count = len(friends_list)
        uniq_groups = set()
        friends_cntr = 0
        user_groups = self.get_user_groups(self.user_id)
        friends_groups = {}
        print('Groups Loaded. Loading friends groups...')
        printprogressbar(0, friends_count, prefix='Progress:', suffix='Complete', length=50)
        for friend in friends_list:
            friends_groups[friend] = self.get_user_groups(friend)
            friends_cntr += 1
            printprogressbar(friends_cntr, friends_count, prefix='Progress:', suffix='Complete', length=50)
            # print('Filling friends groups. Friend {} from {} friends'.format(friends_cntr, friends_count))
            # clear_screen()
        for group in user_groups:
            group_tolerance_cntr = 0
            include_group = True
            for friend_id in friends_groups:
                if group in friends_groups[friend_id]:
                    group_tolerance_cntr += 1
                    if group_tolerance_cntr > self.group_tolerance:
                        include_group = False
                        break
            if include_group:
                uniq_groups.add(group)
        self.user_uniq_groups = uniq_groups

    def write_groups_result(self):
        with open(self.output_file, 'w', encoding="utf-8") as wfile:
            json.dump(fp=wfile, obj=self.groups_info_result, sort_keys=True, indent=4, ensure_ascii=False)

    def run(self):
        if self.auth_fail:
            return
        self.prepare_uniq_groups()
        self.get_groups_info()
        self.write_groups_result()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Vk Uniq Groups Finder.', add_help=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', action='store', help='Vk user id')
    group.add_argument('-u', action='store', help='Vk user name')
    parser.add_argument('-t', dest='g_tolerance', action='store', help='group tolerance')
    parser.add_argument('-o', dest='out_file', action='store', default='outGroups.json', help='File to write results')
    parser.add_argument('-a', dest='auth_data', action='store', required=True,
                        help='Vk AuthToken. Should be passed.')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    else:
        args = parser.parse_args()
    return vars(args)

if __name__ == '__main__':
    start_arguments = parse_arguments()
    if start_arguments['i'] is None:
        uniq_group = VkUniqGroupFinder(start_arguments['auth_data'], user_name=start_arguments['u'],
                                       out_file=start_arguments['out_file'])
    else:
        uniq_group = VkUniqGroupFinder(start_arguments['auth_data'], user_id=start_arguments['i'],
                                       out_file=start_arguments['out_file'])
    if start_arguments['t']:
        uniq_group.group_tolerance = start_arguments['g_tolerance']
    uniq_group.run()
    print('All done. bb hf')
