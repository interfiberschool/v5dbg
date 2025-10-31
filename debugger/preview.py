from prompt_toolkit import print_formatted_text
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
import io

import pygments
from pygments.lexer import Lexer
from pygments.lexers.c_cpp import CppLexer
from pygments.token import Token
from prompt_toolkit.formatted_text import PygmentsTokens, FormattedText

from colors import Colors

"""
Preview the syntax highlighted contents of files within the debugger

When using the 'file' command the debugger will open the file and jump to the correct line number
"""
class FilePreview:
  file_path: str

  file: io.FileIO

  content: str

  def __init__(self, file: str, lexer: Lexer = CppLexer()):
    self.file_path = file

    self.file = open(self.file_path, "r")

    # Read file into memory for parsing

    self.content = self.file.read()

    self.parsed_lines = list()

    for line in self.content.splitlines():
      self.parsed_lines.append(pygments.lex(line, lexer=lexer))

  """
  Print out a single highlighted preview line

  Args:
    line_num (int): Current line number
    line (any): Highlighted line
    selected (bool): Is this line highlighted?
  """
  def print(self, line_num: int, line, selected: bool = False):
      print_formatted_text(FormattedText([
        (f'{Colors.ORANGE if selected else Colors.GRAY}', f'{str(line_num)  }')
      ]), end=" ")


      style = style_from_pygments_cls(get_style_by_name('monokai'))
      print_formatted_text(PygmentsTokens(line), end="", style=style)

  """
  Print out this FilePreview

  Args:
    line (int): Starting line number
    pad (int): Y axis padding
  """
  def print_region(self, line_num: int, pad: int):
    start = line_num - pad
    end = line_num + pad

    i = start + 1

    for line in self.parsed_lines[start:end]:
      self.print(i, line, line_num == i)

      i += 1