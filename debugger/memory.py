from prompt_toolkit import print_formatted_text
import pygments
from subargs import subargs_parse
from protocol import DebuggerMessage, DebuggerMessageType
from utils import DebugInfo
from prompt_toolkit.formatted_text import FormattedText, to_formatted_text, PygmentsTokens
from pygments.token import Token
from pygments.lexers.c_cpp import CppLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name

class Type:
    type_name: str

    # Template to locate, template to replace
    # Use $template for template arguments from base class
    TYPEDEFS = {
        "std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>": "std::string",
        "std::vector<$template>": "std::vector<$targs[0]>"
    }

    def __init__(self, type_name: str):
        self.type_name = type_name

    @classmethod
    def find_template_args(self, template: str):
        start_open = -1
        start_close = -1

        i = 0
        for x in template:
            if x == '<':
                start_open = i
                break
            i += 1

        i = 0

        for x in template:
            if x == '>':
                start_close = i

            i += 1

        if start_open == -1 or start_close == -1:
            return ""

        return template[start_open+1:start_close-1].replace(" ", "")

    # Eval a typedef compression statement
    # param: template = Input template arguments
    # param: stub = Input typedef stub arguments
    @classmethod
    def eval_typedef(self, template: str, stub: str):
        split = template.split(",")
        result = stub.replace("$template", template)

        x = 0
        for i in split:
            result = result.replace(f"$targs[{x}]", i)

            x += 1

        return result

    # Simplify typename by reversing back to pre-defined typedefs, this ends up removing allocator info
    def simp(self):
        t_args = Type.find_template_args(self.type_name)
        for t, replacement in self.TYPEDEFS.items():
            new_def = Type.eval_typedef(t_args, t)

            if new_def == self.type_name.replace(" ", ""): # Templates match, return the simpler version
                return Type.eval_typedef(t_args, replacement)
        
        return self.type_name

    def __str__(self):
        return self.simp()

# Variable exposed to the debug server & debugger via `$expose`
class ProgramVariable:
    name: str
    content: str

    location: DebugInfo
    type: Type

    def __init__(self, name: str, content: str, location: DebugInfo, type: Type):
        self.name = name
        self.content = content
        self.location = location
        self.type = type

    def __str__(self):
        return f"{self.type} {self.name} = {self.content};"

    # Update this variables value with the new debug server state
    def update():
        pass

    # Return the pretty printed version of this variable, updates must be made with update()
    def get(self):
        pass

    def set(self, value):
        # TODO: Tell debugger to set the memory value
        pass

# Contains all raw variable data sent from the debug server
class RawVariableData:
    messages: list[DebuggerMessage]
    variables: list[ProgramVariable]

    def __init__(self, messages: list[DebuggerMessage]):
        self.messages = messages
        self.variables = []

        for m in messages:
            if m.msg_type == DebuggerMessageType.RLMEM:
                self.create_var(m)

    def create_var(self, msg: DebuggerMessage):
        params = subargs_parse(msg.data)
        if len(params) != 5:
            raise Exception("Invalid variable data encoding!")
        
        type = params[0] 
        name = params[1]
        file = params[2]
        line = int(params[3])
        buffer = params[4]

        deb = DebugInfo(file, line)

        self.variables.append(ProgramVariable(name, buffer, deb, Type(type)))

    # Get a variable by name
    def get_variable(self, name: str) -> PygmentsTokens:
        for v in self.variables:
            if v.name == name:
                return PygmentsTokens(list(pygments.lex(str(v), lexer=CppLexer())))

        return None

    # Print all variables managed by this class
    def print_all(self) -> FormattedText:
        if len(self.variables) == 0:
            return to_formatted_text("No variables exposed by debug server")
        
        style = style_from_pygments_cls(get_style_by_name('monokai'))

        for mem in self.variables:
            memory_fmt = f'{mem.type} {mem.name} = {mem.content}; // Allocated at {mem.location}'

            tokens = list(pygments.lex(memory_fmt, lexer=CppLexer()))

            print_formatted_text(PygmentsTokens(tokens), end="", style=style)