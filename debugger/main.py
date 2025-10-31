from commands.run_state import SuspendCommand, ResumeCommand
from comms import DebugServer
from debug import Debugger, DebuggerOptions
from client import DebuggerClient

# Construct the debugger

server = DebugServer(False)
client = DebuggerClient(server)

opts = DebuggerOptions()
debugger = Debugger(opts)

# Register all debugger commands
debugger.register(SuspendCommand())
debugger.register(ResumeCommand())

while True:
    if debugger.ask_execute(client):
        break

server.proc.kill()