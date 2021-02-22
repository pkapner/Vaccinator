#!/usr/bin/env python
import requests
from json import loads

import yaml
from colorama import init, Fore, Style

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

init()
duration = 1
freq = 440

response = requests.get(
    'http://spreadsheets.google.com/feeds/cells/1HzL02Oyax9U-aak9idadwOr6s7SoD1IXBunyiS2L8-8/4/public/full?alt=json',
    verify=False)
data = loads(response.content)
feed = data['feed']


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

with open(dir_path +"/config.yaml") as f:
    docs = yaml.load_all(f, Loader=yaml.FullLoader)
    for doc in docs:
        for k, v in doc.items():
            if k == 'purple':
                purple_set = v
            elif k == 'green':
                green_set = v

myval = json_extract(feed, "$t")

count = 0
available_count = 0
for line in myval:
    if line.startswith('A') or count != 0:
        count = count + 1
        if line.startswith('A') is False:

            # We now have a JSON string representing an entry
            json_line = loads(line)
            available = json_line['is_available']
            if available is True:
                purple_found = False
                green_found = False
                for purple in purple_set:
                    if (json_line['site_name'].find(purple) != -1):
                        purple_found = True
                for green in green_set:
                    if (json_line['site_name'].find(green) != -1):
                        green_found = True
                prefix = Fore.MAGENTA if purple_found else Fore.RESET
                if purple_found:
                    prefix = Fore.MAGENTA
                elif green_found:
                    prefix = Fore.GREEN
                else:
                    prefix = Fore.RESET
                print(prefix + json_line['site_name'])
                print(prefix + json_line['url'])
                print(prefix + str(json_line['appointment_count']) + " appointment slots available")
                available_count = available_count + json_line['appointment_count']
                print(prefix + json_line['appointment_times'])
                print()
            if count == 2:
                count = 0
if available_count > 0:
    print("Available appointments total: " + str(available_count))