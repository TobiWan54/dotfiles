#!/usr/bin/env python

import subprocess
import time
import os
import signal

with open('/tmp/waybar/night-light', 'r') as file:
    night_light = file.read();

if night_light == '0':
    with open('/tmp/waybar/night-light', 'w') as file:
        file.write('1')
    subprocess.Popen(['gammastep', '-P', '-O', '3000'], start_new_session=True)
else:
    with open('/tmp/waybar/night-light', 'w') as file:
        file.write('0')
    processes = subprocess.run(['pgrep', 'gammastep'], capture_output=True, text=True).stdout.split()
    for process in processes:
        os.kill(int(process), signal.SIGTERM)