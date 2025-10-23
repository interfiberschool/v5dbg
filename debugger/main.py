from comms import DebugServer
from debugger import debug_stacktrace, debug_threads
from protocol import DebuggerMessage,DebuggerMessageType

server = DebugServer()

while server.connected():
    cmd = input("% ")

    if cmd == "suspend" or cmd == "pause" or cmd == "p":
        server.proc.stdin.write(b"%1:1:0\n")
        server.proc.stdin.flush()

        print("Program execution paused")
    elif cmd == "resume" or cmd == "continue" or cmd == "c":
        server.proc.stdin.write(b"%1:4:0\n")
        server.proc.stdin.flush()

        print("Program execution resumed")
    elif cmd == "threads" or cmd == "th":
        server.proc.stdin.write(b"%1:5:0\n")
        server.proc.stdin.flush()

        debug_threads(server.wait_for(DebuggerMessageType.RTHREADS))
    elif cmd == "bt" or cmd == "backtrace" or cmd == "stack":
        server.proc.stdin.write(b"%1:7:0\n")
        server.proc.stdin.flush()

        result = server.get_msg_range(DebuggerMessageType.RVSTACK, DebuggerMessageType.VSTACK_END)

        debug_stacktrace(result)
    else:
        print("Unknown command:", cmd)