#!/usr/bin/env python

import time
import subprocess
import sys
import json
import os
import signal


def report():

    data = {}
    percentage = -1

    try:
        percentage = int(subprocess.run(['sudo', 'mxw', 'report', 'battery'], capture_output=True, text=True).stdout[:-2])
    except (ValueError, IndexError):
        data['class'] = 'unavailable'
        data['alt'] = 'unavailable'
    else:
        if percentage <= 20:
            data['class'] = 'critical'
            data['alt'] = 'critical'
        else:
            data['class'] = ''
            data['alt'] = ''
    data['percentage'] = percentage

    print(json.dumps(data), flush=True)

    return percentage


# Kill old process if relevant.
try:
    with open('/tmp/waybar/mouse-battery-pid', 'r') as file:
        os.kill(int(file.read()), signal.SIGKILL)
except (FileNotFoundError, ProcessLookupError):
    pass

with open('/tmp/waybar/mouse-battery-pid', 'w') as file:
    file.write(str(os.getpid()))


# First attempts, scaling up in retry time.
for i in range(10):
    if report() == -1:
        time.sleep(2+i^3)
    else:
        break
    

while True:

    time.sleep(1800)
    report()