from enum import IntEnum
from comms import DebugServer
from protocol import DebuggerMessage, DebuggerMessageType
from utils import print_list

# Debugger state bitflags
class DebuggerState(IntEnum):
    RUN = 1 << 0
    SUSPEND = 1 << 2

# Thread managed by the remote v5dbg server 
class DebuggerThread:
    thread_id: int
    server: DebugServer

    def __init__(self, server: DebugServer, thread_id: int):
        self.server = server
        self.thread_id = thread_id

    # Return the backtrace for this thread
    def backtrace(self):
        pass

# Local debugger client class
class DebuggerClient:
    state: DebuggerState
    active_thread: DebuggerThread
    server: DebugServer

    def __init__(self, server: DebugServer):
        self.server = server

        self.active_thread = DebuggerThread(self.server, 0)

    # Send a message to the remote server
    def send_msg(self, message: DebuggerMessage):
        self.server.write(message.serialize())
    
    # Switch the active thread to `thread_id`
    def switch_thread(self, thread_id: int):
        self.active_thread = DebuggerThread(self.server, thread_id)

    # Print out the current threads stack trace
    def print_stacktrace(self):
        # Ask debugger for virtual callstack

        vstack_for = DebuggerMessage(DebuggerMessageType.VSTACK_FOR)
        vstack_for.data = str(self.active_thread.thread_id)

        self.send_msg(vstack_for)

        # Compile message list

        stacktrace = []
        messages = self.server.get_msg_range(DebuggerMessageType.RVSTACK, DebuggerMessageType.VSTACK_END)

        for x in messages:
            if x.msg_type == DebuggerMessageType.VSTACK_END:
                break

            if x.msg_type == DebuggerMessageType.RVSTACK:
                stacktrace.append(x.data)

        print("Current thread:")
        print("---------------")

        stacktrace.reverse() # Reverse so the newest function is on top; the debug server has the newest function on the bottom
        print_list(stacktrace)


    # Print out the list of supervised threads to the console
    def print_threads(self):
        # Ask for thread listing

        get_threads = DebuggerMessage(DebuggerMessageType.THREADS)
        self.send_msg(get_threads)

        # Wait for thread data
        thread_data = self.server.wait_for(DebuggerMessageType.RTHREADS)
        if len(thread_data) == 0:
            print("Invalid thread ID for threads()")
        else:
            print("Supervised thread listing:")
            print("-----------------------")

            thread_blob = str()

            for x in thread_data:
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


