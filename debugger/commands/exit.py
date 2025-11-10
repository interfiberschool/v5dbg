import sys
from client.client import DebuggerClient
from cli.debug import CommandExecutor, Debugger

"""
Exit debugger command
"""


class ExitCommand(CommandExecutor):
    def __init__(self):
        pass

    def register(self, parser):
        parser.add_parser(
            "exit", help="Exit the debugger while leaving the user program running"
        )

    def get_name(self):
        return "exit"

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        if command.debugger == "exit":
            client.server.proc.kill()
            sys.exit(0)
