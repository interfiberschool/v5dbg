import argparse

from colors import Colors
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from client import DebuggerClient
from debug import CommandExecutor, Debugger
from protocol import DebuggerMessage,DebuggerMessageType

"""
Suspend state command
"""
class SuspendCommand(CommandExecutor):
    def __init__(self):
        pass

    def register(self, parser): 
        parser.add_parser('suspend', help='Suspend the execution of all supervised tasks', aliases=['halt', 's'])

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        if command.debugger == 'suspend' or command == 'halt' or command.debugger == 's':

            # Send message to suspend program
            suspend = DebuggerMessage(DebuggerMessageType.SUSPEND)

            client.send_msg(suspend)

            print_formatted_text(FormattedText([
                ('', "Program has been "),
                (Colors.STEEL, "SUSPENDED")
            ]))

"""
Resume state command
"""
class ResumeCommand(CommandExecutor):
    def __init__(self):
        pass

    def register(self, parser): 
        parser.add_parser('resume', help='Resume the execution of all supervised tasks', aliases=['continue', 'c'])

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        if command.debugger == 'c' or command.debugger == 'continue':
        # Send message to suspend program
        suspend = DebuggerMessage(DebuggerMessageType.SUSPEND)

        client.send_msg(suspend)

        print_formatted_text(FormattedText([
            ('', "Program has been "),
            (Colors.STEEL, "SUSPENDED")
        ]))