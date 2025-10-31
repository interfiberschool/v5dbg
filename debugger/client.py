from enum import IntFlag, auto

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from comms import DebugServer
from breakpoint import DebuggerBreakpoint
from colors import Colors
from stack import StackFrame
from thread import DebuggerThread
from protocol import DebuggerMessage, DebuggerMessageType

# Debugger state bit flags
class DebuggerState(IntFlag):
    RUN = auto()
    SUSPEND = auto()

# Local debugger client class
class DebuggerClient:
    state: DebuggerState
    active_thread: DebuggerThread
    active_break: DebuggerBreakpoint
    server: DebugServer

    def __init__(self, server: DebugServer):
        self.server = server
        self.state = DebuggerState.RUN

        self.active_thread = DebuggerThread(0, self.server)

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

    """
    Callback used when a breakpoint is tripped
    """
    def break_tripped_handler(self, msg: DebuggerMessage):
      b = DebuggerBreakpoint(msg)

      b.print_tripped()

      # Mark program to be in the suspend state
      self.state |= DebuggerState.SUSPEND
      self.state = self.state & ~DebuggerState.RUN

      # Find current stack frame
      bt = self.get_stacktrace()

      # Select the given frame in the backtrace that this breakpoint belongs too
      for frame in bt:
          if frame.name == b.function:
              print_formatted_text(FormattedText([
                  ('', "Moving to frame "),
                  (Colors.CYAN, b.function),
                  ('', ' in '),
                  (Colors.ORANGE, str(b.location))
              ]))

              self.active_thread.frame_index = frame.id

              break

      print_formatted_text("Program suspended for breakpoint, use 'continue' to resume execution")

      self.active_break = b

    """
    Enable/disable a breakpoint by numerical ID
    """
    def enable_breakpoint(self, id: int, enabled: bool = True):
      if id < 0:
          print_formatted_text(f'Breakpoint ID must be positive!')
          return

      msg = DebuggerMessage(DebuggerMessageType.BREAKPOINT_SET_STATUS)
      msg.data = f'{str(id)}:{int(enabled)}'

      self.send_msg(msg)

      print_formatted_text(f'Breakpoint #{id} {"enabled" if enabled else "disabled"}')

    # Return the current frame's stack memory
    def get_memory(self):
        return self.active_thread.get_memory()

    """
    Return the stacktrace for the active thread
    """
    def get_stacktrace(self, inject_breaks: bool = False) -> list[StackFrame]:
        # Ask debugger for virtual callstack

        b = self.active_thread.get_backtrace()

        if not inject_breaks or self.active_break == None:
            return b
        
        # Inject breakpoints by changing the frame information where the breakpoint is located
        for frame in b:
            if frame.name == self.active_break.function and frame.file == self.active_break.location.file:
                frame.line = self.active_break.location.line
                break

        return b

    # Suspend all supervised threads
    def suspend(self):
        self.state |= DebuggerState.SUSPEND
        self.state = self.state & ~DebuggerState.RUN

        suspend = DebuggerMessage(DebuggerMessageType.SUSPEND)
        self.send_msg(suspend)
    
    # Resume all supervised threads
    def resume(self):
        self.state |= DebuggerState.RUN
        self.state = self.state & ~DebuggerState.SUSPEND
        self.active_break = None

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
                    if int(blob) == self.active_thread.id:
                        c_thread = True

                    print(f"({blob}) ", end="")
                else:
                    print(f"{blob} {"[Current]" if c_thread else ""}")
                    c_thread = False

                i += 1


