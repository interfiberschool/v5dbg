from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from colors import Colors
from utils import DebugInfo
from subargs import subargs_parse
from protocol import DebuggerMessage

class DebuggerBreakpoint:
  id: int
  location: DebugInfo
  function: str

  def __init__(self, msg: DebuggerMessage):
    args = subargs_parse(msg.data)

    self.id = int(args[0])
    self.function = args[1]
    self.location = DebugInfo(args[2], int(args[3]))

  """
  Print breakpoint information
  """
  def print_info(self):
    print_formatted_text(FormattedText([
      ('', f'#{self.id} '),
      (Colors.ORANGE, f'{self.function} '),
      ('', 'at '),
      (Colors.CYAN, str(self.location))
    ]))

  def print_tripped(self):
    print_formatted_text(FormattedText([
      ('', f'Breakpoint #{self.id} tripped at '),
      (Colors.CYAN, str(self.location))
    ]))
