#!/usr/bin/env python

import subprocess
import time

with open('/tmp/waybar/brightness', 'r') as file:
    old_brightness = int(file.read())

if old_brightness <= 10:
    new_brightness = 0
else:
    new_brightness = old_brightness - 10

# Quickly write target brightness to file so it can be read by update script and other threads.
with open('/tmp/waybar/brightness', 'w') as file:
    file.write(str(new_brightness))

# Give some time for other threads to write to file.
# time.sleep(1)

# Refresh old brightness while waiting until no other threads are accessing ddcutil.
try:
    old_brightness = int(subprocess.run(['ddcutil', 'getvcp', '10', '-t'], capture_output=True, text=True).stdout.split()[-2])
except (ValueError, IndexError): # in case of locking
    pass

# Refresh new brightness.
with open('/tmp/waybar/brightness', 'r') as file:
    new_brightness = int(file.read())
    
if new_brightness != old_brightness:
    subprocess.run(['ddcutil', 'setvcp', '10', str(new_brightness)])
