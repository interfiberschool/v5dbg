from enum import IntFlag, auto
from comms import DebugServer
from thread import DebuggerThread
from memory import RawVariableData
from protocol import DebuggerMessage, DebuggerMessageType
from utils import print_list

# Debugger state bit flags
class DebuggerState(IntFlag):
    RUN = auto()
    SUSPEND = auto()

# Local debugger client class
class DebuggerClient:
    state: DebuggerState
    active_thread: DebuggerThread
    server: DebugServer
    current_frame: int

    def __init__(self, server: DebugServer):
        self.server = server
        self.state = DebuggerState.RUN

        self.active_thread = DebuggerThread(0, self.server)
        self.current_frame = 0

    # Send a message to the remote server
    def send_msg(self, message: DebuggerMessage):
        self.server.write(message.serialize())
    
    # Switch the active thread to `thread_id`
    def switch_thread(self, thread_id: int):
        self.active_thread = DebuggerThread(thread_id, self.server)

    # Print debugger state
    def print_state(self):
        if self.state & DebuggerState.RUN:
            print("Program is: RUNNING")

        if self.state & DebuggerState.SUSPEND:
            print("Program is: SUSPENDED")

    # Return the current frame's stack memory
    def get_memory(self):
        return self.active_thread.get_memory()

    # Return a list of StackFrame objects for the current thread
    def get_stacktrace(self):
        # Ask debugger for virtual callstack

        if self.state & DebuggerState.RUN:
            print("Program must be in the SUSPEND state for a stacktrace to be generated")
            return

        return self.active_thread.get_backtrace()

    # Suspend all supervised threads
    def suspend(self):
        if self.state & DebuggerState.SUSPEND:
            print("Program is not in the RUN state")
            return False

        self.state |= DebuggerState.SUSPEND
        self.state = self.state & ~DebuggerState.RUN

        suspend = DebuggerMessage(DebuggerMessageType.SUSPEND)
        self.send_msg(suspend)
    
    # Resume all supervised threads
    def resume(self):
        if self.state & DebuggerState.RUN:
            print("Program is not in the SUSPEND state")
            return False

        self.state |= DebuggerState.RUN
        self.state = self.state & ~DebuggerState.SUSPEND

        resume = DebuggerMessage(DebuggerMessageType.RESUME)
        self.send_msg(resume)

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
            c_thread = False
            for blob in thread_blob_split:
                if i % 2 == 0:
                    if int(blob) == self.active_thread.thread_id:
                        c_thread = True

                    print(f"({blob}) ", end="")
                else:
                    print(f"{blob} {"[Current]" if c_thread else ""}")
                    c_thread = False

                i += 1


