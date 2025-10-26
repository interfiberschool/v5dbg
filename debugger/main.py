import argparse
import atexit
import os
import client
from comms import DebugServer
from protocol import PROTOCOL_VERSION, DebuggerMessage,DebuggerMessageType
import platform

ENABLE_READLINE = True

if platform.system() != 'Windows':
  import readline
else:
    ENABLE_READLINE = False

# CLI arg parser
program = argparse.ArgumentParser(prog='v5dbg',description='Debugger client for the remote v5dbg server')
program.add_argument("--no-open-wait", help="Don't wait for the debug server to send an OPEN message to begin debugging", action="store_true")

args = program.parse_args()

HISTORY_LENGTH = 1000

print("Welcome to the v5dbg debugger client!")
print("We're running protocol version: " + str(PROTOCOL_VERSION))
print("Current platform: " + platform.platform() + " on " + platform.architecture()[1] + " " + platform.architecture()[0] + " running Python " + platform.python_version())
print("---------------------------------------------------------\n")

parser = argparse.ArgumentParser(
    prog='v5dbg',
    description='Debugger client for the remote v5dbg server',
    epilog='(Written by Hunter from 8568T) https://github.com/Interfiber/v5dbg'
)

debugger = parser.add_subparsers(help='Debugger commands', dest='debugger')

help = debugger.add_parser('help', help="Show this page", aliases=['h', '?'])

bt = debugger.add_parser('bt', help='Print the backtrace for the current thread', aliases=['backtrace', 'stack'])
suspend = debugger.add_parser('suspend', help='Suspend the execution of all supervised threads', aliases=['halt', 's'])
resume = debugger.add_parser('resume', help='Resume the execution of all supervised threads', aliases=['continue', 'c'])
state = debugger.add_parser('state', help='Print the debugger\'s state')
mem = debugger.add_parser('mem', help='View local stack memory')
print_var = debugger.add_parser('print', help='Print local stack memory objects', aliases=['p'])
print_var.add_argument('variable_id', help='Name of the local variable to print', type=str, action="store")
exit = debugger.add_parser('exit', help='Exit the debugger and disconnect from the comms server', aliases=['q'])

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

if ENABLE_READLINE:
  try:
      readline.read_history_file(histfile)
      # default history len is -1 (infinite), which may grow unruly
      readline.set_history_length(HISTORY_LENGTH)
  except FileNotFoundError:
    pass

  atexit.register(readline.write_history_file, histfile)

client = client.DebuggerClient(server)

while server.connected():
    cmd = input("(v5dbg) ")

    try:
        parsed = parser.parse_args(cmd.split())
    except:
        # Retry
        continue

    # print(parsed)

    if parsed.debugger == 'bt' or parsed.debugger == 'backtrace' or parsed.debugger == 'stack':
        stacktrace = client.get_stacktrace()
        if stacktrace == None:
            continue

        for s in stacktrace:
            print(f"# {s}")
    elif parsed.debugger == 'suspend' or parsed.debugger == 'halt' or parsed.debugger == 's':
        if client.suspend() == None:
            print("All supervised threads have been suspended")
    elif parsed.debugger == 'resume' or parsed.debugger == 'continue' or parsed.debugger == 'c':
        if client.resume() == None:
            print("All supervised threads have resumed execution")
    elif parsed.debugger == 'state':
        client.print_state()
    elif parsed.debugger == 'mem':
        print(client.get_memory().all())
    elif parsed.debugger == 'exit' or parsed.debugger == 'q':
        print("Byte!")
        break

    if parsed.debugger == 'help' or parsed.debugger == 'h' or parsed.debugger == '?':
        parser.print_help()

    if parsed.debugger == 'thread':
        if parsed.thread == 'set':
            client.switch_thread(parsed.thread_id)

            print(f"Switch active debugger thread to {parsed.thread_id}")
        elif parsed.thread == 'l' or parsed.thread == 'list':
            client.print_threads()
        elif parsed.thread == None:
            client.print_threads()
    
    if parsed.debugger == 'print' or parsed.debugger == 'p':
        var = client.get_memory().get_variable(parsed.variable_id)

        if var == None:
            print(f"No variable with name '{parsed.variable_id}' is current scope")
        else:
            print(var)

print("Disconnected from comms server, exiting...")
server.proc.kill()