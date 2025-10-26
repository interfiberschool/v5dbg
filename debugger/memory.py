from subargs import subargs_parse
from protocol import DebuggerMessage, DebuggerMessageType
from utils import DebugInfo

class Type:
    type_name: str

    def __init__(self, type_name: str):
        self.type_name = type_name

    def __str__(self):
        return self.type_name

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
        d = ""
        for mem in self.variables:
            d += f"  {mem.type} {mem.name} = <Allocated at {mem.location}>\n"

        return d