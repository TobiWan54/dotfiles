#!/usr/bin/env python

import json
import subprocess
import sys
import os
import signal

# Not sure exactly how it works, but get_tree returns multidimensional lists of (floating_)nodes.
# Iterating as deeply as possible through these lists returns all PIDs.
def iterate(nodes, pid):
    for node in nodes:
        if 'pid' in node:
            pids.append(node['pid'])
        iterate(node['nodes'], pids)
        iterate(node['floating_nodes'], pids)

# Get tree and convert into dictionary.
tree = subprocess.run(['swaymsg', '-t', 'get_tree', '--raw'], capture_output=True, text=True).stdout
tree = json.loads(tree)

# Iterate down through the nodes and floating_nodes lists to populate a list of PIDs.
pids = []
iterate(tree['nodes'], pids)
iterate(tree['floating_nodes'], pids)

# Kill all PIDs, except child PIDs already killed with parent.
for pid in pids:
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass