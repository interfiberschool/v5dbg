import argparse

from breakpoint import DebuggerBreakpoint
from preview import FilePreview
from protocol import DebuggerMessageType, DebuggerMessage
from prompt_toolkit import PromptSession, formatted_text, print_formatted_text
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import NestedCompleter
from client import DebuggerClient, DebuggerState
from colors import Colors
from comms import DebugServer
from prompt_toolkit.history import FileHistory


# CLI arg parser
program = argparse.ArgumentParser(prog='v5dbg',description='Debugger client for the remote v5dbg server')
program.add_argument("--no-open-wait", help="Don't wait for the debug server to send an OPEN message to begin debugging", action="store_true")

args = program.parse_args()

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

frame = debugger.add_parser('frame', help='Set/get the current frame index')
frame.add_argument('frame_index', help='Frame index to set which can be obtained from "backtrace"', type=int, action="store", nargs="?")

exit = debugger.add_parser('exit', help='Exit the debugger and disconnect from the comms server', aliases=['q'])

preview = debugger.add_parser('preview', help='Preview the region near the current stack frame\'s', aliases=['pr'])

file_cmd = debugger.add_parser('file', help='Pretty print the contents of a file')
file_cmd.add_argument('file_path', help='(Optional) Path to the file to display, defaults to the current stack frame', type=str, action="store", nargs="?")

break_cmd = debugger.add_parser('break', help='Manage breakpoints', aliases=['b'])
break_sub = break_cmd.add_subparsers(help='Breakpoint commands', dest='breakp')

break_enable = break_sub.add_parser('enable', help='Enable the given breakpoint by ID')
break_enable.add_argument("breakpoint_id", help="Breakpoint ID to enable", action="store", type=int)

break_disable = break_sub.add_parser('disable', help='Disable the given breakpoint by ID')
break_disable.add_argument("breakpoint_id", help="Breakpoint ID to disable", action="store", type=int)

thread = debugger.add_parser('thread', help='Manage supervised threads')
thread_sub = thread.add_subparsers(help='Thread commands', dest="thread")

thread_set = thread_sub.add_parser('set', help="Set the currently active thread ID")
thread_set.add_argument("thread_id", help="Thread ID to set", action="store", type=int)

thread_list = thread_sub.add_parser('list', help="List all supervised threads", aliases=["l"])

server = DebugServer(not args.no_open_wait)

client = DebuggerClient(server)
server.set_breakpoint_trip(client.break_tripped_handler)

# Main command loop

session = PromptSession(history=FileHistory(".v5dbg_history"))

# NOTE: This has to be updated with current command list
completer = NestedCompleter.from_nested_dict({
    # Exit/quit
    "exit": None,
    "mem": None,
    "state": None,
    "resume": None,
    "suspend": None,
    "continue": None,
    "help": None,
    "backtrace": None,
    "stack": None,
    "break": {
        "enable": {
            "break_id": None
        },
        "disable": {
            "break_id": None
        }
    },
    "preview": None,
    "print": {
        "variable_name": None
    },
    "frame": {
        "frame_id": None
    },
    "thread": {
        "set": {
            "thread_id": None
        }
    }
})

while True:
    cmd = session.prompt("(v5dbg) % ", vi_mode=True, auto_suggest=AutoSuggestFromHistory(), completer=completer, cursor=CursorShape.BLOCK)

    try:
        parsed = parser.parse_args(cmd.split())
    except:
        # Retry
        continue

    # print(parsed)

    if parsed.debugger == 'bt' or parsed.debugger == 'backtrace' or parsed.debugger == 'stack':
        stacktrace = client.get_stacktrace(True)
        if stacktrace == None:
            continue

        for s in stacktrace:
            print_formatted_text(formatted_text.FormattedText([
                ("", f"#{s.id} "),
                (Colors.ORANGE, f"{s.name} "),
                ("", "from "),
                (Colors.CYAN, f"{s.file}:{s.line}")
                ]))
    elif parsed.debugger == 'suspend' or parsed.debugger == 'halt' or parsed.debugger == 's':
        if client.suspend() == None:
            print_formatted_text("All supervised threads have been suspended")
    elif parsed.debugger == 'resume' or parsed.debugger == 'continue' or parsed.debugger == 'c':
        if client.resume() == None:
            print_formatted_text("All supervised threads have resumed execution")
    elif parsed.debugger == 'state':
        client.print_state()
    elif parsed.debugger == 'mem':
        client.get_memory().print_all()
    elif parsed.debugger == 'exit' or parsed.debugger == 'q':
        print_formatted_text("Bye!")
        break
    elif parsed.debugger == 'preview' or parsed.debugger == 'pr':
        if client.state & DebuggerState.RUN:
          print("Program must be SUSPENDED for file preview to be given")
          continue

        bt = client.get_stacktrace(True)
        frame = bt[client.active_thread.frame_index]

        preview = FilePreview(frame.file)
        preview.print_region(frame.line, 8)

    if parsed.debugger == 'help' or parsed.debugger == 'h' or parsed.debugger == '?':
        parser.print_help()

    if parsed.debugger == 'thread':
        if parsed.thread == 'set':
            client.switch_thread(parsed.thread_id)

            print_formatted_text(f"Switch active debugger thread to {parsed.thread_id}")
        elif parsed.thread == 'l' or parsed.thread == 'list':
            client.print_threads()
        elif parsed.thread == None:
            client.print_threads()
    
    if parsed.debugger == 'print' or parsed.debugger == 'p':
        var = client.get_memory().get_variable(parsed.variable_id)

        if var == None:
            print_formatted_text(f"No variable with name '{parsed.variable_id}' is current scope")
        else:
            style = style_from_pygments_cls(get_style_by_name('emacs'))
            print_formatted_text(var, style=style, end="")

    if parsed.debugger == 'frame':
        if parsed.frame_index == None:
            print_formatted_text(f"Current stack frame: #{client.active_thread.frame_index}")
        else:
            client.active_thread.frame_index = parsed.frame_index

            print_formatted_text(f"Switched to frame #{client.active_thread.frame_index}")
    
    if parsed.debugger == 'break' or parsed.debugger == 'b':
        if parsed.breakp == 'enable':
            client.enable_breakpoint(parsed.breakpoint_id)
        elif parsed.breakp == 'disable':
            client.enable_breakpoint(parsed.breakpoint_id, False)
        else:
          list_breaks = DebuggerMessage(DebuggerMessageType.LBREAKPOINTS)

          client.send_msg(list_breaks)

          msgs = server.get_msg_range(DebuggerMessageType.RBREAKPOINT, DebuggerMessageType.RBREAKPOINT)

          for msg in msgs:
              if msg.msg_type != DebuggerMessageType.RBREAKPOINT:
                continue

              DebuggerBreakpoint(msg).print_info()

server.proc.kill()