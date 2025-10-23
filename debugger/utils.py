# Various utils

import os

# Find the local server executable to init comms with remote debug server
def find_server():
    if os.path.exists('v5dbg-server'):
        return 'v5dbg-server'
    elif os.path.exists('./bin/v5dbg-server'):
        return './bin/v5dbg-server'
    elif os.path.exists('./v5dbg-server/target/debug/v5dbg-server'):
        return './v5dbg-server/target/debug/v5dbg-server'

    return None

def print_list(list):
    for x in list:
        print(x)