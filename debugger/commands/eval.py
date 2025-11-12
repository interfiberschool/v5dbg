import sys

from prompt_toolkit import print_formatted_text
from client.client import DebuggerClient
from cli.debug import CommandExecutor, Debugger

"""
Eval python code using memory from the current scope
"""


class EvalCommand(CommandExecutor):
    def __init__(self):
        pass

    def register(self, parser):
        p = parser.add_parser(
            "evalpy", help="Eval python code using variables from the current debugger scope"
        )

        p.add_argument("eval_py", help="Python statement to eval", type=str, action="store")

    def get_name(self):
        return "evalpy"

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        if command.debugger == "evalpy":
            statement = command.eval_py 

            memory = client.get_memory()

            locals = dict()

            for var in memory.variables:
                locals[var.name] = var.content

            result = eval(statement, locals=locals)
            print_formatted_text(str(result))
