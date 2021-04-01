#!/usr/bin/env python
import requests
from json import loads

import yaml
from colorama import init, Fore

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

init()
duration = 1
freq = 440

with open(dir_path + "/config.yaml") as f:
    docs = yaml.load_all(f, Loader=yaml.FullLoader)
    for doc in docs:
        for k, v in doc.items():
            if k == 'purple':
                purple_set = v
            elif k == 'green':
                green_set = v
            elif k == 'site':
                site = v

response = requests.get(str(site), verify=False)
feed = loads(response.content)
portals = feed['portals']
data = feed['locations']
portal_dict = {}

for portal in portals:
    portal_dict[portal['key']] = portal['url']

def json_extract(obj, key):
    arr = []

    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


count = 0
available_count = 0
for line in data:
    # print(str(line))
    # print(portal_dict[line['portal']])
    # continue

    available = line['available']
    if available is True:
        purple_found = False
        green_found = False
        for purple in purple_set:
            if (line['name'].find(purple) != -1):
                purple_found = True
        for green in green_set:
            if (line['name'].find(green) != -1):
                green_found = True
        prefix = Fore.MAGENTA if purple_found else Fore.RESET
        if purple_found:
            prefix = Fore.MAGENTA
        elif green_found:
            prefix = Fore.GREEN
        else:
            prefix = Fore.RESET
        print(prefix + line['name'])
        print(prefix + line['area'])
        print(prefix + portal_dict[line['portal']])
        print(prefix + str(line['appointment_count']) + " appointment slots available")
        available_count = available_count + line['appointment_count']
        print(prefix + line['appointment_times'])
        print()
    if count == 2:
        count = 0
if available_count > 0:
    print("Available appointments total: " + str(available_count))
