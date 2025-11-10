import argparse

from cli.colors import Colors
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from client.client import DebuggerClient, DebuggerState
from cli.debug import CommandExecutor, Debugger
from server.protocol import DebuggerMessage, DebuggerMessageType

"""
Suspend state command
"""
class SuspendCommand(CommandExecutor):
    def __init__(self):
        pass

    def register(self, parser):
        parser.add_parser('suspend', help='Suspend the execution of all supervised tasks', aliases=['halt', 's'])

    def get_name(self):
        return "suspend"

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        if command.debugger == 'suspend' or command == 'halt' or command.debugger == 's':
            if client.state & DebuggerState.SUSPEND:
                print_formatted_text(FormattedText([
                    ('', "Program is not in the "),
                    (Colors.RED, "RUN "),
                    ('', 'state')
                ]))
                return

            client.suspend()

            print_formatted_text(FormattedText([
                ('', "Program state: "),
                (Colors.STEEL, "SUSPEND")
            ]))

"""
Resume state command
"""
class ResumeCommand(CommandExecutor):
    def __init__(self):
        pass

    def get_name(self):
        return "resume"

    def register(self, parser):
        parser.add_parser('resume', help='Resume the execution of all supervised tasks', aliases=['continue', 'c'])

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        if command.debugger == 'resume' or command.debugger == 'c' or command.debugger == 'continue':

            if client.state & DebuggerState.RUN:
                print_formatted_text(FormattedText([
                    ('', "Program is not in the "),
                    (Colors.RED, "SUSPEND "),
                    ('', 'state')
                ]))
                return

            # Resume program
            client.resume()

            print_formatted_text(FormattedText([
                ('', "Program state: "),
                (Colors.STEEL, "RUN")
            ]))
