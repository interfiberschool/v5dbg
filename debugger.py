import subprocess
import threading as thread
import os
from enum import IntEnum

# Find the local server executable to init comms with remote debug server
def find_server():
    if os.path.exists('v5dbg-server'):
        return 'v5dbg-server'
    elif os.path.exists('./bin/v5dbg-server'):
        return './bin/v5dbg-server'
    elif os.path.exists('./v5dbg-server/target/debug/v5dbg-server'):
        return './v5dbg-server/target/debug/v5dbg-server'

    return None

PROTOCOL_VERSION = 1

# For documentation on these types see include/v5dbg/protocol.h
class DebuggerMessageType(IntEnum):
    OPEN = 0,
    SUSPEND = 1,
    CLOSE = 2,
    ALLOC_STRING = 3,
    RESUME = 4,
    THREADS = 5,
    RTHREADS = 6,
    VSTACK_FOR = 7,
    RVSTACK = 8,
    VSTACK_END = 9,
    LMEM_FOR = 10,
    RLMEM = 11,
    LMEM_END = 12

class DebuggerMessage():
    msg_type: DebuggerMessageType
    parameters: list

    # The third parameter....
    data: str

    def __init__(self, data: str):
        if data[0] != '%': # Should never executed since the DebugServer checks for this to determine messages
            raise Exception("Incoming debugger message does not start with a '%'")

        # Most of this code was ported from src/v5dbg/protocol.cpp/V5Dbg_DeserializeMessage
        # Might not be the best code ever...
        # 10/22/25

        parameters = []
        collectedArguments = 0
        message = ""

        for c in data:
            if c == ':' and collectedArguments < 2:
                collectedArguments += 1

                parameters.append(message)
                message = ""
            else:
                message += c
        
        if collectedArguments < 2:
            raise Exception("Not enough parameters for message! Expected 2 and got " + collectedArguments)
        
        parameters.append(message)

        parameters[0] = parameters[0][1:]
        parameters[len(parameters) - 1] = parameters[len(parameters) - 1].strip()

        if int(parameters[0]) != PROTOCOL_VERSION:
            raise Exception("Debugger message has invalid protocol version, expected: " + PROTOCOL_VERSION + " and got: " + parameters[0])

        self.msg_type = DebuggerMessageType(int(parameters[1]))
        self.parameters = parameters
        self.data = self.parameters[2]

def print_list(list):
    for x in list:
        print(x)

# Generate a proper thread list from RTHREADS
def debug_threads(messages: list[DebuggerMessage]):
    print("Managed thread listing:")
    print("-----------------------")

    thread_blob = str()

    for x in messages:
        if x.msg_type == DebuggerMessageType.RTHREADS:
            # Store thread data blob
            thread_blob = x.data
            break

    thread_blob_split = thread_blob.split(",")
    thread_blob_split.reverse()

    i = 0
    for blob in thread_blob_split:
        if i % 2 == 0:
            print(f"({blob}) ", end="")
        else:
            print(blob)

        i += 1



# Generate a proper stacktrace list from VSTACK messages
def debug_stacktrace(messages: list[DebuggerMessage]):
    # Debug server gives us bottom-up but we want top down so the most recent function appears on top

    stacktrace = []

    for x in messages:
        if x.msg_type == DebuggerMessageType.VSTACK_END:
            break

        if x.msg_type == DebuggerMessageType.RVSTACK:
            stacktrace.append(x.data)

    print("Current thread:")
    print("---------------")

    stacktrace.reverse() # Reverse so the newest function is on top; the debug server has the newest function on the bottom
    print_list(stacktrace)

class DebugServer:
    waits: dict[DebuggerMessageType, thread.Condition]
    wait_results: dict[DebuggerMessageType, list[DebuggerMessage]]

    MESSAGE_TRACE_MAX = 100

    # Messages analyzed by get_msg_range, which automatically clears this.
    # NOTE: If get_msg_range is not called enough it will be auto cleaned by the message IO thread
    message_trace: list[DebuggerMessage]

    def __init__(self):
        self.server_path = find_server()
        self.proc = subprocess.Popen(['./v5dbg-server/target/debug/v5dbg-server'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.waits = dict()
        self.wait_results = dict()
        self.message_trace = list()

        self.io = thread.Thread(target=self.io_thread)
        self.io.start()

    # Return True if we are connected to the remote debug server
    def connected(self):
        return self.proc.poll() == None

    # Stockpile messages until msg_type is found
    # NOTE: This function blocks until completion, use carefully
    def get_msg_range(self, front: DebuggerMessageType, end: DebuggerMessageType):
        self.wait_for(end)

        # Copy all messages from message history

        trace_reversed = self.message_trace
        trace_reversed.reverse()

        end_index = 0
        front_index = 0

        # Find end index
        x = 0

        for t in trace_reversed:
            if t.msg_type == end:
                end_index = x # Keep improving until we find the latest
            
            x += 1
        
        x = 0

        for t in trace_reversed:
            if t.msg_type == front:
                front_index = x # Keep improving until we find the latest

            x += 1

        splice = trace_reversed[end_index:front_index + 1]
        splice.reverse()

        self.message_trace.clear() # Auto clear our message trace so we don't get confused with old messages when we get called again

        return splice


    # Wait for the next message of the given type to arrive
    def wait_for(self, msg_type: DebuggerMessageType, count: int = -1):
        if msg_type in self.waits:
            raise Exception("Thread already waiting for that message!")

        self.waits[msg_type] = thread.Condition()

        with self.waits[msg_type]:
            self.waits[msg_type].wait()

        self.waits.pop(msg_type)

        if count == -1:
            return self.wait_results[msg_type]
        elif count != len(self.wait_results[msg_type]):
            print("re-run wait_for to meet count")
            return self.wait_for(msg_type, count)
        elif count == len(self.wait_results[msg_type]):
            return self.wait_results[msg_type]

    # IO thread for reading messages from the debug server (remote)
    def io_thread(self):
        while self.proc.poll() == None:
            b = self.proc.stdout.readline()

            # First 6 bytes are useless to us as they only contain stream information
            data = b[6:].decode()
            if len(data) == 0:
                continue

            if data[0] != '%':
                continue

            msg = DebuggerMessage(data)

            if len(self.message_trace) + 1 > self.MESSAGE_TRACE_MAX:
                self.message_trace.clear()
            
            self.message_trace.append(msg)

            if msg.msg_type in self.waits:
                if not msg.msg_type in self.wait_results:
                    self.wait_results[msg.msg_type] = list()

                self.wait_results[msg.msg_type].append(msg)

                with self.waits[msg.msg_type]:
                    self.waits[msg.msg_type].notify_all()

server = DebugServer()

while server.connected():
    cmd = input("% ")

    if cmd == "suspend" or cmd == "pause" or cmd == "p":
        server.proc.stdin.write(b"%1:1:0\n")
        server.proc.stdin.flush()

        print("# Program execution paused")
    elif cmd == "resume" or cmd == "continue" or cmd == "c":
        server.proc.stdin.write(b"%1:4:0\n")
        server.proc.stdin.flush()

        print("# Program execution resumed")
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