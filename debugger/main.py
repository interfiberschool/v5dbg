from commands.run_state import SuspendCommand, ResumeCommand
from comms import DebugServer
from debug import Debugger, DebuggerOptions
from client import DebuggerClient
from commands.backtrace import BacktraceCommand
from commands.memory import MemoryCommand, PrintCommand
from commands.frame import FrameCommand
from commands.preview import PreviewCommand
from commands.breakp import BreakCommand

# Construct the debugger

server = DebugServer(False)
client = DebuggerClient(server)

# Setup breakpoint tripped handler
server.set_breakpoint_trip(client.break_tripped_handler)

opts = DebuggerOptions()
debugger = Debugger(opts, client)

# Register all debugger commands
debugger.register(SuspendCommand())
debugger.register(ResumeCommand())
debugger.register(BacktraceCommand())
debugger.register(MemoryCommand())
debugger.register(PrintCommand())
debugger.register(FrameCommand())
debugger.register(PreviewCommand())
debugger.register(BreakCommand())

while True:
    if debugger.ask_execute():
        break

server.proc.kill()
