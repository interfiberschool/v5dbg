# Debugger utility functions

from protocol import DebuggerMessage, DebuggerMessageType
from utils import print_list

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

