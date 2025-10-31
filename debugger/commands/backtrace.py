from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from colors import Colors
from client import DebuggerClient, DebuggerState
from debug import CommandExecutor, Debugger

"""
Program backtrace command
"""
class BacktraceCommand(CommandExecutor):
    def __init__(self):
        pass

    def register(self, parser): 
        parser.add_parser('backtrace', help='Print the backtrace for the active thread', aliases=['bt', 'stack'])

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        if command.debugger == 'backtrace' or command.debugger == 'bt' or command.debugger == 'stack':

            if client.state & DebuggerState.RUN:
                print_formatted_text(FormattedText([
                    ('', "Program is not in the "),
                    (Colors.RED, "SUSPEND "),
                    ('', 'state')
                ]))
                return
            
            stacktrace = client.get_stacktrace(True)

            for s in stacktrace:
                print_formatted_text(FormattedText([
                    ("", f"#{s.id} "),
                    (Colors.ORANGE, f"{s.name} "),
                    ("", "from "),
                    (Colors.CYAN, f"{s.file}:{s.line}")
                    ]))