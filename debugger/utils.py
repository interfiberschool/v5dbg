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

class DebugInfo:
    file: str
    line: int

    def __init__(self, file: str, line: str):
        self.file = file
        self.line = line

    # Create a DebugInfo instance using an encoded string formatted as:
    # FILE_PATH:LINE_NUMBER
    @classmethod
    def from_str(self, data: str):
        dsplit = data.split(":")
        if len(dsplit) != 2:
            raise Exception("from_str expected FILE:LINE encoded input")

        return DebugInfo(dsplit[0], int(dsplit[1]))
    
    def __str__(self):
        return f"{self.file}:{self.line}"
    
# Stolen from stackoverflow btw
class ANSICodes:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'