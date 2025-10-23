import argparse
import atexit
import os
import client
from comms import DebugServer
from debugger import debug_stacktrace, debug_threads
from protocol import PROTOCOL_VERSION, DebuggerMessage,DebuggerMessageType
import readline

# CLI arg parser
program = argparse.ArgumentParser(prog='v5dbg',description='Debugger client for the remote v5dbg server')
program.add_argument("--no-open-wait", help="Don't wait for the debug server to send an OPEN message to begin debugging", action="store_true")

args = program.parse_args()

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

thread = debugger.add_parser('thread', help='Manage supervised threads')
thread_sub = thread.add_subparsers(help='Thread commands', dest="thread")

thread_set = thread_sub.add_parser('set', help="Set the currently active thread ID")
thread_set.add_argument("thread_id", help="Thread ID to set", action="store", type=int)

thread_list = thread_sub.add_parser('list', help="List all supervised threads", aliases=["l"])

print("Connecting to local communications server...")

server = DebugServer(not args.no_open_wait)

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

client = client.DebuggerClient(server)

while server.connected():
    cmd = input("% ")

    try:
        parsed = parser.parse_args(cmd.split())
    except:
        # Retry
        continue

    print(parsed)

    if parsed.debugger == 'bt' or parsed.debugger == 'backtrace' or parsed.debugger == 'stack':
        server.proc.stdin.write(b"%1:7:0\n")
        server.proc.stdin.flush()

        result = server.get_msg_range(DebuggerMessageType.RVSTACK, DebuggerMessageType.VSTACK_END)

        debug_stacktrace(result)

    if parsed.debugger == 'thread':
        if parsed.thread == 'set':
            client.switch_thread(parsed.thread_id)

            print(f"Switch active debugger thread to {parsed.thread_id}")
        elif parsed.thread == 'l' or parsed.thread == 'list':
            client.print_threads()
        elif parsed.thread == None:
            client.print_threads()

            print(f"\nActive thread ID: {client.active_thread.thread_id}")


print("Disconnected from comms server, exiting...")