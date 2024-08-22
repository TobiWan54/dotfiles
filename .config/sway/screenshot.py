#!/usr/bin/env python

import sys
import subprocess
import time
import os


home = os.getenv("HOME")


if len(sys.argv) != 3:
    sys.exit(f'Usage:\n  {sys.argv[0]} (copy|save|copysave) (region|screen)')


if sys.argv[1] == 'copy':
    copy = True
    save = False
elif sys.argv[1] == 'copysave':
    copy = True
    save = True
elif sys.argv[1] == 'save':
    copy = False
    save = True
else:
    sys.exit(f'Invalid argument {sys.argv[1]}. Must be copy, save or copysave.')


if sys.argv[2] == 'region':

    region = subprocess.check_output(['slurp']).decode('utf8').strip()
    
    if save:
        path = f'{home}/Documents/Screenshots/{time.strftime('%y-%m-%d-%H:%M:%S')}'
        subprocess.run(['grim', '-g', region, path])
        
        if copy:
            with open(path, 'rb') as file:
                subprocess.run(['wl-copy'], input=file.read())
    
    else:
        image = subprocess.check_output(['grim', '-g', region, '-'])
        subprocess.run(['wl-copy'], input=image)


elif sys.argv[2] == 'screen':

    if save:
        path = f'{home}/Documents/Screenshots/{time.strftime('%y-%m-%d-%H:%M:%S')}'
        subprocess.run(['grim', path])

        if copy:
            with open(path, 'rb') as file:
                subprocess.run(['wl-copy'], input=file.read())

    else:
        image = subprocess.check_output(['grim', '-'])
        subprocess.run(['wl-copy'], input=image)

else:
    sys.exit(f'Invalid argument {sys.argv[2]}. Must be region or screen.')

if save:
    subprocess.run(['notify-send', '-a', 'grim', '-i', path, 'Screenshot', path])
elif copy:
    subprocess.run(['notify-send', '-a', 'grim', '-i', 'edit-copy', 'Screenshot', 'Copied to clipboard.'])
