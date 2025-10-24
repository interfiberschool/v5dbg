# Handles debugger program thread objects

class DebuggerThread:
  id: int
  frame_index: int

  def __init__(self, id: int):
    self.id = id
    self.frame_index = 0

  # Return the backtrace string for this thread
  def backtrace(self):
    pass     