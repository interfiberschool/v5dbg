from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from client import DebuggerClient
from debug import CommandExecutor, Debugger
from stack import StackFrame
from colors import Colors

"""
Set and get the current stack frame
"""
class FrameCommand(CommandExecutor):
    cached_stack: list[StackFrame]

    def __init__(self):
        self.cached_stack = None
        pass
    
    def next_completion(self, command: str, current_arg: int, current_text: str, c_index: int, client: DebuggerClient) -> str:
      if command != 'frame': return None
      if current_arg != 1: return None

      if self.cached_stack == None:
        self.cached_stack = client.get_stacktrace()

      if c_index >= len(self.cached_stack):
        return None
        
      return str(self.cached_stack[c_index].id)

    def register(self, parser): 
      f = parser.add_parser('frame', help='Set and get the current stack frame')
      f.add_argument('frame_id', help='ID of the frame to make active', type=int, action="store", nargs="?")

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
       if command.debugger == 'frame':
          if command.frame_id == None:
             frame_id = client.active_thread.frame_index

             print_formatted_text(FormattedText([
                ('', 'Current frame ID: '),
                (Colors.STEEL, f'#{frame_id}')
             ]))

          else:
            trace = client.active_thread.get_backtrace()
            frame_id = command.frame_id

            if frame_id + 1 > len(trace) or frame_id < 0:
               print_formatted_text(FormattedText([
                  (Colors.RED, 'Invalid stack frame!')
               ]))
            else:
              client.active_thread.frame_index = frame_id

              print_formatted_text(FormattedText([
                ('', 'New frame ID: '),
                (Colors.STEEL, f'#{frame_id}')
              ]))


