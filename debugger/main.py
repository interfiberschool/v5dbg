import argparse
import atexit
import os
from comms import DebugServer
from debugger import debug_stacktrace, debug_threads
from protocol import PROTOCOL_VERSION, DebuggerMessage,DebuggerMessageType
import readline

HISTORY_LENGTH = 1000

print("Welcome to the v5dbg debugger client!")
print("We're running protocol version: " + str(PROTOCOL_VERSION))
print("---------------------------------------------------------\n")

parser = argparse.ArgumentParser(
    prog='v5dbg',
    description='Debugger client for the remote v5dbg server',
    epilog='(Written by Hunter from 8568T) https://github.com/Interfiber/v5dbg'
)

debugger = parser.add_subparsers(help='Debugger commands', dest='debugger')

bt = debugger.add_parser('bt', help='Print the backtrace for the current thread', aliases=['backtrace', 'stack'])

print("Connecting to local communications server...")
server = DebugServer()

print("Connected to remote debug server! Environment is ready to go!")

histfile = os.path.join(os.path.expanduser("~"), ".v5dbg_history")

print(f"Your command history is being loaded from '{histfile}' with a total of {HISTORY_LENGTH} items")

try:
    readline.read_history_file(histfile)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(HISTORY_LENGTH)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)

while server.connected():
    cmd = input("% ")

    try:
        parsed = parser.parse_args(cmd.split())
    except:
        # Retry
        continue

    if parsed.debugger == 'bt':
        server.proc.stdin.write(b"%1:7:0\n")
        server.proc.stdin.flush()

        result = server.get_msg_range(DebuggerMessageType.RVSTACK, DebuggerMessageType.VSTACK_END)

        debug_stacktrace(result)

print("Disconnected from comms server, exiting...")