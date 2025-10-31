from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from client import DebuggerClient
from debug import CommandExecutor, Debugger
from stack import StackFrame
from protocol import DebuggerMessage, DebuggerMessageType
from breakpoint import DebuggerBreakpoint
from colors import Colors

"""
Enable and list breakpoints
"""
class FrameCommand(CommandExecutor):
    cached_stack: list[StackFrame]

    def __init__(self):
        self.cached_stack = None
        pass
    
    def next_completion(self, command: str, current_arg: int, current_text: str, c_index: int, client: DebuggerClient) -> str:
      if command != 'break': return None
      if current_arg != 1: return None

      if self.cached_stack == None:
        self.cached_stack = client.get_stacktrace()

      if c_index >= len(self.cached_stack):
        return None
        
      return str(self.cached_stack[c_index].id)

    def register(self, parser): 
      break_cmd = parser.add_parser('break', help='Manage breakpoints', aliases=['b'])
      break_sub = break_cmd.add_subparsers(help='Breakpoint commands', dest='breakp')

      break_enable = break_sub.add_parser('enable', help='Enable the given breakpoint by ID')
      break_enable.add_argument("breakpoint_id", help="Breakpoint ID to enable", action="store", type=int)

      break_disable = break_sub.add_parser('disable', help='Disable the given breakpoint by ID')
      break_disable.add_argument("breakpoint_id", help="Breakpoint ID to disable", action="store", type=int)



    def execute(self, client: DebuggerClient, debugger: Debugger, command):
       if command.debugger == 'break':
          if command.breakp == 'enable':
            client.enable_breakpoint(int(command.breakpoint_id), True)

            print_formatted_text(FormattedText([
               ('', 'Enabled breakpoint '),
               (Colors.STEEL, f'#{id(command.breakpoint_id)}')
            ]))

          elif command.breakp == 'disable':
            client.enable_breakpoint(int(command.breakpoint_id), False)

            print_formatted_text(FormattedText([
               ('', 'Disabled breakpoint '),
               (Colors.STEEL, f'#{id(command.breakpoint_id)}')
            ]))
          else:
            list_breaks = DebuggerMessage(DebuggerMessageType.LBREAKPOINTS)

            client.send_msg(list_breaks)

            msgs = client.server.get_msg_range(DebuggerMessageType.RBREAKPOINT, DebuggerMessageType.RBREAKPOINT)

            for msg in msgs:
              if msg.msg_type != DebuggerMessageType.RBREAKPOINT:
                continue

              DebuggerBreakpoint(msg).print_info()
