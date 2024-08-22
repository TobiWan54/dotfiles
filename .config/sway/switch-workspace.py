#!/usr/bin/env python

import json
import subprocess
import sys

workspaces = subprocess.run(['swaymsg', '-t', 'get_workspaces', '--raw'], capture_output=True, text=True).stdout
workspaces = json.loads(workspaces)

for workspace in workspaces:
    if workspace['focused']:
        number = workspace['num']

if sys.argv[1] == 'next':
    if number < 10:
        number += 1
elif sys.argv[1] == 'prev':
    if number > 1:
        number -= 1

subprocess.run(['swaymsg', 'workspace', str(number)])