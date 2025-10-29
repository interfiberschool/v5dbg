from subargs import subargs_parse
from protocol import DebuggerMessage, DebuggerMessageType
from utils import DebugInfo

class Type:
    type_name: str

    # Template to locate, template to replace
    # Use $template for template arguments from base class
    TYPEDEFS = {
        "std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >": "std::string",
        "std::vector<$template>": "std::vector<$template>"
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
        return stub.replace("$template", template)        

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
    def get_variable(self, name: str):
        for v in self.variables:
            if v.name == name:
                return v

        return None

    # Print all variables managed by this class
    def all(self):
        if len(self.variables) == 0:
            return "No variables exposed by debug server\n"

        d = ""
        for mem in self.variables:
            d += f"  {mem.type} {mem.name} = <Allocated at {mem.location}>\n"

        return d