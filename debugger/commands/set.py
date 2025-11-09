from client import DebuggerClient
from colors import Colors
from debug import CommandExecutor, Debugger
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from protocol import DebuggerMessage, DebuggerMessageType, DebuggerVariableSetMode

"""
Handles setting memory within the local frame context
"""


class SetCommand(CommandExecutor):
    def __init__(self):
        pass

    def get_name(self):
        return "set"

    def register(self, parser):
        p = parser.add_parser("set", help="Set the value of a variable")
        p2 = parser.add_parser("setc", help="Set the value of a variable across reallocations")

        parsers = [p, p2]

        for p_parser in parsers:
            p_parser.add_argument(
                "variable_id",
                help="Name of the local variable to set the value of",
                type=str,
                action="store",
            )

            p_parser.add_argument(
                "value_buffer",
                help="Value to set the variable to",
                type=str,
                action="store",
            )

    def next_completion(
        self,
        command: str,
        current_arg: int,
        current_text: str,
        c_index: int,
        client: DebuggerClient,
    ) -> str:
        return None

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        if command.debugger != "set" and command.debugger != "setc":
            return

        set_mode = DebuggerVariableSetMode.SINGLE if command.debugger == "set" else DebuggerVariableSetMode.CONST

        name = command.variable_id
        buffer = command.value_buffer

        set_msg = DebuggerMessage(DebuggerMessageType.MEMORY_SET)
        set_msg.data = f"[{name}]:[{buffer}]:{client.active_thread.frame_index}:{client.active_thread.id}:{set_mode}"

        client.send_msg(set_msg)

        # Wait for the debug server response
        response = client.server.wait_for(DebuggerMessageType.RMEMORY_SET)
        response_code = response[0].data

        if response_code == "AllocatorFailure":
            print_formatted_text(
                FormattedText(
                    [
                        (
                            Colors.RED,
                            "The debug server buffer allocator failed to allocate your input data",
                        )
                    ]
                )
            )
            return
        elif response_code == "ConversionFailure":
            print_formatted_text(
                FormattedText(
                    [
                        (
                            Colors.RED,
                            "The debug server buffer allocator failed to convert your input string",
                        )
                    ]
                )
            )
            return
        elif response_code == "NoAllocator":
            print_formatted_text(
                FormattedText(
                    [
                        (
                            Colors.RED,
                            "The debug server could not find a suitable allocator registered with $pretty_printer_allocator",
                        )
                    ]
                )
            )
            return
        elif response_code == "NoVariable":
            print_formatted_text(
                FormattedText(
                    [
                        (
                            Colors.RED,
                            f"No variable in the current scope with the name '{name}'",
                        )
                    ]
                )
            )
            return

        print_formatted_text(
            FormattedText(
                [
                    ("", "Set value of variable "),
                    (Colors.ORANGE, name),
                    ("", " to "),
                    (Colors.STEEL, buffer),
                ]
            )
        )
