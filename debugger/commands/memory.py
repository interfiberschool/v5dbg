from debug import CommandExecutor, Debugger
from debugger.client import DebuggerClient, DebuggerState
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit import print_formatted_text

"""
Displays memory within the current stack frame
"""
class MemoryCommand(CommandExecutor):
    def __init__(self):
        pass

    def register(self, parser): 
        parser.add_parser('mem', help='Print exposed memory within the local stack frame')

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        if command.debugger == 'mem':
            client.get_memory().print_all()