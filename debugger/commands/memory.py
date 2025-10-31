from debug import CommandExecutor, Debugger
from client import DebuggerClient
from memory import RawVariableData
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit import print_formatted_text
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
from colors import Colors

"""
Print the value of a variable
"""
class PrintCommand(CommandExecutor):
  cached_memory: RawVariableData

  def __init__(self):
      self.cached_memory = None
  
  def register(self, parser):
    p = parser.add_parser('print', help='Print a variable by name', aliases=['p'])
    p.add_argument('variable_id', help='Name of the local variable to print', type=str, action="store")

  def next_completion(self, command: str, current_arg: int, current_text: str, c_index: int, client: DebuggerClient) -> str:
    if command != 'print': return None
    if current_arg != 1: return None

    if self.cached_memory == None:
      self.cached_memory = client.get_memory()

    if c_index >= len(self.cached_memory.variables):
      return None
        
    return self.cached_memory.variables[c_index].name


  def execute(self, client: DebuggerClient, debugger: Debugger, command):
    if command.debugger == 'print' or command.debugger == 'p':
      var = client.get_memory().get_variable(command.variable_id)

      if var == None:
         print_formatted_text(FormattedText([
            (Colors.RED, f'No variable in current scope with name \'{command.variable_id}\'')
         ]))
      else:
        style = style_from_pygments_cls(get_style_by_name('monokai'))
        print_formatted_text(var, end="", style=style)

"""
Displays memory within the current stack frame
"""
class MemoryCommand(CommandExecutor):
    def __init__(self):
        pass

    def register(self, parser): 
        parser.add_parser('mem', help='List exposed memory within the local stack frame')

    def execute(self, client: DebuggerClient, debugger: Debugger, command):
        if command.debugger == 'mem':
          client.get_memory().print_all()