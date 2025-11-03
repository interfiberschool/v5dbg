from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from client import DebuggerClient, DebuggerState
from debug import CommandExecutor, Debugger
from colors import Colors
from preview import FilePreview

"""
Preview the code around the current frames file and line
"""


class PreviewCommand(CommandExecutor):
    def __init__(self):
        pass

    def register(self, parser):
        parser.add_parser(
            "preview",
            help="Preview the contents of the file around the current frame",
            aliases=["pr"],
        )

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        if command.debugger == "preview" or command.debugger == "pr":
            # Only allow preview during suspend

            if client.state & DebuggerState.RUN:
                print_formatted_text(
                    FormattedText(
                        [
                            ("", "Program is not in the "),
                            (Colors.RED, "SUSPEND "),
                            ("", "state"),
                        ]
                    )
                )
                return
            
            st = client.get_stacktrace(True)
            if len(st) == 0:
                return
            
            # Obtain last stack frame
            last_frame = st[client.active_thread.frame_index]

            # Print file preview
            preview = FilePreview(last_frame.file)
            preview.print_region(last_frame.line, 8)