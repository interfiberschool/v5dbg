from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from client.client import DebuggerClient
from cli.debug import CommandExecutor, Debugger
from client.stack import StackFrame
from server.protocol import DebuggerMessage, DebuggerMessageType
from client.breakpoint import DebuggerBreakpoint
from cli.colors import Colors

"""
Enable and list breakpoints
"""


class BreakCommand(CommandExecutor):
    cached_stack: list[StackFrame]

    COMMANDS: list[str] = [
        "enable",
        "disable"
    ]

    def __init__(self):
        self.cached_stack = None
        pass

    def get_name(self):
      return "break"

    def next_completion(
        self,
        command: str,
        current_arg: int,
        current_text: str,
        c_index: int,
        client: DebuggerClient,
    ) -> str:
        if command != "break": return None

        if current_arg == 1 and c_index < len(self.COMMANDS):
          return self.COMMANDS[c_index - 1]

        return None

    def register(self, parser):
        break_cmd = parser.add_parser("break", help="Manage breakpoints", aliases=["b"])
        break_sub = break_cmd.add_subparsers(help="Breakpoint commands", dest="breakp")

        break_enable = break_sub.add_parser(
            "enable", help="Enable the given breakpoint by ID"
        )
        break_enable.add_argument(
            "breakpoint_id", help="Breakpoint ID to enable", action="store", type=str
        )

        break_disable = break_sub.add_parser(
            "disable", help="Disable the given breakpoint by ID"
        )
        break_disable.add_argument(
            "breakpoint_id", help="Breakpoint ID to disable", action="store", type=str
        )

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        if command.debugger == "break":
            if command.breakp == "enable":
                breakp_id = -1

                if command.breakpoint_id.isnumeric():
                    breakp_id = int(command.breakpoint_id)
                else:
                    new_name = client.get_stack_frame().name + command.breakpoint_id

                    # Find location information
                    split = command.breakpoint_id.split(":")
                    file = split[0]
                    line = 0
                    if len(split) == 2 and split[1].isnumeric():
                        line = int(split[1])

                    for bpoint in client.get_breakpoints(True):
                        if bpoint.function == new_name or (bpoint.location.file == file and bpoint.location.line == line):
                            breakp_id = bpoint.id
                            break

                if client.enable_breakpoint(breakp_id, True) == None:
                    return

                print_formatted_text(
                    FormattedText(
                        [
                            ("", "Enabled breakpoint "),
                            (Colors.STEEL, f"#{breakp_id}"),
                        ]
                    )
                )

            elif command.breakp == "disable":
                breakp_id = -1

                if command.breakpoint_id.isnumeric():
                    breakp_id = int(command.breakpoint_id)
                else:
                    new_name = client.get_stack_frame().name + command.breakpoint_id

                    # Find location information
                    split = command.breakpoint_id.split(":")
                    file = split[0]
                    line = 0
                    if len(split) == 2 and split[1].isnumeric():
                        line = int(split[1])

                    for bpoint in client.get_breakpoints(True):
                        if bpoint.function == new_name or (bpoint.location.file == file and bpoint.location.line == line):
                            breakp_id = bpoint.id
                            break

                if client.enable_breakpoint(breakp_id, False) == None:
                    return

                print_formatted_text(
                    FormattedText(
                        [
                            ("", "Disabled breakpoint "),
                            (Colors.STEEL, f"#{breakp_id}"),
                        ]
                    )
                )
            else:
              for b in client.get_breakpoints():
                b.print_info()
