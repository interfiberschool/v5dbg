from enum import IntFlag, auto
from comms import DebugServer
from stack import StackFrame
from protocol import DebuggerMessage, DebuggerMessageType
from utils import print_list

# Debugger state bitflags
class DebuggerState(IntFlag):
    RUN = auto()
    SUSPEND = auto()

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
    current_frame: int

    def __init__(self, server: DebugServer):
        self.server = server
        self.state = DebuggerState.RUN

        self.active_thread = DebuggerThread(self.server, 0)
        self.current_frame = 0

    # Send a message to the remote server
    def send_msg(self, message: DebuggerMessage):
        self.server.write(message.serialize())
    
    # Switch the active thread to `thread_id`
    def switch_thread(self, thread_id: int):
        self.active_thread = DebuggerThread(self.server, thread_id)

    # Print debugger state
    def print_state(self):
        if self.state & DebuggerState.RUN:
            print("Program is: RUNNING")

        if self.state & DebuggerState.SUSPEND:
            print("Program is: SUSPENDED")

    def print_memory(self):
        mem = DebuggerMessage(DebuggerMessageType.LMEM_FOR)
        mem.data = str(self.current_frame) + "," + str(self.active_thread.thread_id)

        self.send_msg(mem)

        memory = self.server.get_msg_range(DebuggerMessageType.RLMEM, DebuggerMessageType.LMEM_END)

        for x in memory:
            if x.msg_type != DebuggerMessageType.RLMEM:
                continue

            data_split = x.data.split(",")

            debinfo = data_split[len(data_split) - 1] # Debug info is the last item in the split array

            pretty_printer = data_split[0:len(data_split) - 1] # Variables like vectors have spaces so just merge everything up until (not including) the final one into a string again

            print('# ' + ", ".join(pretty_printer))
            print(f"  Allocated at {debinfo}")

    # Return a list of StackFrame objects for the current thread
    def get_stacktrace(self):
        # Ask debugger for virtual callstack

        if self.state & DebuggerState.RUN:
            print("Program must be in the SUSPEND state for a stacktrace to be generated")
            return

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
                stacktrace.append(StackFrame.from_msg(x.data))

        return stacktrace

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


