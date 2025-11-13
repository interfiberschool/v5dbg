"""
Interactive debugger options
"""

import argparse
import sys
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from client.client import DebuggerClient, DebuggerState
from config import DebuggerConfig
from client.stack import StackFrame


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


class Debugger(Completer):
    opts: DebuggerOptions
    session: PromptSession
    commands: list
    parser: argparse.ArgumentParser
    client: DebuggerClient
    cached_stack: list[StackFrame]

    def __init__(self, options: DebuggerOptions, client: DebuggerClient):
        self.opts = options
        self.commands = []
        self.client = client
        self.cached_stack = []

        self.parser = argparse.ArgumentParser(
            prog="v5dbg",
            description="Debugger client for the remote v5dbg server",
            epilog="(Written by Hunter from 8568T) https://github.com/Interfiber/v5dbg",
        )

        self.parser_debugger = self.parser.add_subparsers(
            help="Debugger commands", dest="debugger"
        )

        self.session = PromptSession(history=FileHistory(self.opts.hist_file))

    """
    Register a new command
    """

    def register(self, executor):
        self.commands.append(executor)

        executor.register(self.parser_debugger)

    def get_completions(self, document, complete_event):
        split = document.text.split(" ")

        if len(split) == 1:
            for command in self.commands:
                if command.get_name().startswith(split[0]):
                    yield Completion(command.get_name(), start_position=0)
        else:
            for command in self.commands:
                i = 0
                while True:
                    result = command.next_completion(
                        split[0], len(split) - 1, split[len(split) - 1], i, self.client
                    )

                    if result != None:
                        # Empty items won't get pushed
                        if result != "":
                            yield Completion(result, start_position=0)
                    else:
                        break

                    i += 1



    """
    Used by the prompt to return the current stack frame
    """
    def get_toolbar_frame(self):
        if self.client.state == DebuggerState.SUSPEND:
            frame = self.cached_stack[self.client.active_thread.frame_index]
            return f" | {frame.name} in {frame.file}"
        else:
            return ''

    """
    Ask for a debugger command and execute it
    """

    def ask_execute(self):
        try:
            cmd = self.session.prompt(
                self.opts.prompt,
                vi_mode=True,
                auto_suggest=AutoSuggestFromHistory(),
                completer=self,
                bottom_toolbar=lambda: HTML(DebuggerConfig.left() + ' | ' + f'{'[Breakpoint] ' if self.client.active_break is not None else ''}' + ('[Suspended]' if self.client.state == DebuggerState.SUSPEND else '[Executing]') + self.get_toolbar_frame())
            )
        except EOFError:
            sys.exit(0)
        except:
            return True

        # Crude argument splitter

        arguments = []
        arg = ""
        skip_mode = False

        for c in cmd.strip():
            if c == " " and not skip_mode:
                arguments.append(arg)
                arg = ""
                continue
            elif c == "\"":
                skip_mode = not skip_mode
                continue

            arg += c

        arguments.append(arg)

        try:
            parsed = self.parser.parse_args(arguments)
        except:
            self.cached_stack = self.client.get_stacktrace(True)
            return False

        for exe in self.commands:
            exe.execute(self.client, self, parsed)


        self.cached_stack = self.client.get_stacktrace(True)

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

    def get_name(self) -> str:
        raise NotImplementedError("subclass should implement get_name(...)")

    """
    Generate the next completion item for this command

    Returning None will stop calling this function, returning an empty string will call again without pushing a new completion item
    """

    def next_completion(
        self,
        command: str,
        current_arg: int,
        current_text: str,
        c_index: int,
        client: DebuggerClient,
    ) -> str:
        return None
