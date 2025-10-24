# Various utils

import os
import platform

def exe(file):
    if platform.system() == 'Windows':
        return file + ".exe"
    
    return file

# Find the local server executable to init comms with remote debug server
def find_server():
    if os.path.exists(exe('./bin/v5dbg-server')):
        return exe('./bin/v5dbg-server')
    elif os.path.exists(exe('./v5dbg-server/target/debug/v5dbg-server')):
        return exe('./v5dbg-server/target/debug/v5dbg-server')

    return None

def print_list(list):
    id = 0
    for x in list:
        print(x, abs(id - len(list) + 1))

        id += 1