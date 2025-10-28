# Handles stack frames captured by the debug server
from subargs import subargs_parse


class StackFrame:
    # Name of the stack frame, unmangled usually this is the function name obtained from __PRETTY_FUNCTION__
    name: str

    # Source file which this stack frame is located in
    file: str

    # Line number that this stack frame begins on
    line: int

    # ID of this stack frame, top frame on the stack is location zero
    id: int

    def __init__(self, name: str, file: str, line: int, id: int = -1):
        self.name = name
        self.file = file
        self.line = line
        self.id = id

    # Create a StackFrame object using the data of a RVSTACK message
    # Encoding should be: ID:NAME:FILE:LINE_NUMBER 
    @classmethod
    def from_msg(self, buffer: str):
        bsplit = subargs_parse(buffer)
        
        # If we fail to cast any of these then we just die, we trust the debug server with our life tho...

        id = int(bsplit[0])
        name = bsplit[1] 
        loc_file = bsplit[2]
        loc_line = int(bsplit[3])

        return StackFrame(name, loc_file, loc_line, id)

    def __str__(self):
        return f"{f"({self.id})" if self.id != -1 else ""} {self.name} at {self.file}:{self.line}"