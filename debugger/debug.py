
"""
Interactive debugger options
"""

import argparse
from prompt_toolkit.history import FileHistory
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from client import DebuggerClient

class DebuggerOptions:
    """
    Should we wait for the debug server to send an OPEN message before entering interactive mode?
    """
    wait_for_open: bool

    """
    File to save history too
    """
    hist_file: str = ".v5dbg_history"

    """
    Interactive prompt
    """
    prompt: str = "(v5dbg) "

"""
Main v5dbg interactive class
"""
class Debugger:
    opts: DebuggerOptions
    session: PromptSession
    commands: list
    parser: argparse.ArgumentParser

    def __init__(self, options: DebuggerOptions):
        self.opts = options
        self.commands = []

        self.parser = argparse.ArgumentParser(
            prog='v5dbg',
            description='Debugger client for the remote v5dbg server',
            epilog='(Written by Hunter from 8568T) https://github.com/Interfiber/v5dbg'
        )

        self.parser_debugger = self.parser.add_subparsers(help='Debugger commands', dest='debugger')

        self.session = PromptSession(
            history=FileHistory(self.opts.hist_file)
        )

    """
    Register a new command
    """
    def register(self, executor):
        self.commands.append(executor)

        executor.register(self.parser_debugger)

    """
    Ask for a debugger command and execute it
    """
    def ask_execute(self, client: DebuggerClient):
        try:
            cmd = self.session.prompt(self.opts.prompt, vi_mode=True, auto_suggest=AutoSuggestFromHistory(),)
        except EOFError:
            exit(0)
        except:
            return True
        
        try:
            parsed = self.parser.parse_args(cmd.split())
        except:
            return False

        for exe in self.commands:
            exe.execute(client, self, parsed)

        return False

"""
Base debugger command class
"""
class CommandExecutor:
    parser: argparse.ArgumentParser

    """
    Register this CommandExecutor with the argument parser
    """
    def register(self, parser):
        raise NotImplementedError("Subclass should implement register(...)")

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        raise NotImplementedError("Subclass should implement execute(...)") 