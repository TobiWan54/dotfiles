#!/usr/bin/env python

import os
import subprocess
import time
import json

data = {}

try:
    with open('/tmp/waybar/brightness', 'r') as file:
        data['percentage'] = int(file.read())
except FileNotFoundError:
    try:
        percentage = subprocess.run(['ddcutil', 'getvcp', '10', '-t'], capture_output=True, text=True).stdout.split()[3]
        data['percentage'] = int(percentage)
        with open('/tmp/waybar/brightness', 'w') as file:
            file.write(percentage)
    except (IndexError, ValueError):
        pass

try:
    with open('/tmp/waybar/night-light') as file:
        night_light = file.read()
    if night_light == '1':
        data['alt'] = 'night-light'
        data['class'] = 'night-light'
    else:
        data['alt'] = "asdf"
        data['class'] = "asdfasdf"
except FileNotFoundError:
    with open('/tmp/waybar/night-light', 'w') as file:
        file.write('0')

print(json.dumps(data))
