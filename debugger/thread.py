# Handles debugger program thread objects

from comms import DebugServer
from memory import RawVariableData
from protocol import DebuggerMessageType, DebuggerMessage
from stack import StackFrame

class DebuggerThread:
  id: int
  frame_index: int
  server: DebugServer

  def __init__(self, id: int, server: DebugServer):
    self.id = id
    self.frame_index = 0
    self.server = server

  def get_memory(self):
    mem = DebuggerMessage(DebuggerMessageType.LMEM_FOR)
    mem.data = f"{self.frame_index},{self.id}"

    self.server.write(mem.serialize())

    memory = self.server.get_msg_range(DebuggerMessageType.RLMEM, DebuggerMessageType.LMEM_END)

    return RawVariableData(memory)

  # Return the backtrace string for this thread
  def get_backtrace(self):
    vstack_for = DebuggerMessage(DebuggerMessageType.VSTACK_FOR)
    vstack_for.data = str(self.id)

    self.server.write(vstack_for.serialize())

    # Compile message list

    stacktrace = []
    messages = self.server.get_msg_range(DebuggerMessageType.RVSTACK, DebuggerMessageType.VSTACK_END)

    for x in messages:
      if x.msg_type == DebuggerMessageType.VSTACK_END:
        break

      if x.msg_type == DebuggerMessageType.RVSTACK:
        stacktrace.append(StackFrame.from_msg(x.data))

    return stacktrace