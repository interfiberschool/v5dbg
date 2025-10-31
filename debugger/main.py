from commands.run_state import SuspendCommand, ResumeCommand
from comms import DebugServer
from debug import Debugger, DebuggerOptions
from client import DebuggerClient
from commands.backtrace import BacktraceCommand
from commands.memory import MemoryCommand, PrintCommand

# Construct the debugger

server = DebugServer(False)
client = DebuggerClient(server)

opts = DebuggerOptions()
debugger = Debugger(opts, client)

# Register all debugger commands
debugger.register(SuspendCommand())
debugger.register(ResumeCommand())
debugger.register(BacktraceCommand())
debugger.register(MemoryCommand())
debugger.register(PrintCommand())

while True:
    if debugger.ask_execute():
        break

server.proc.kill()