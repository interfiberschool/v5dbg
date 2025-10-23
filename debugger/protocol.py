# For documentation on these types see include/v5dbg/protocol.h
from enum import IntEnum

PROTOCOL_VERSION = 1

class DebuggerMessageType(IntEnum):
    OPEN = 0,
    SUSPEND = 1,
    CLOSE = 2,
    ALLOC_STRING = 3,
    RESUME = 4,
    THREADS = 5,
    RTHREADS = 6,
    VSTACK_FOR = 7,
    RVSTACK = 8,
    VSTACK_END = 9,
    LMEM_FOR = 10,
    RLMEM = 11,
    LMEM_END = 12

class DebuggerMessage():
    msg_type: DebuggerMessageType
    parameters: list

    # The third parameter....
    data: str

    def __init__(self, data: str):
        if data[0] != '%': # Should never executed since the DebugServer checks for this to determine messages
            raise Exception("Incoming debugger message does not start with a '%'")

        # Most of this code was ported from src/v5dbg/protocol.cpp/V5Dbg_DeserializeMessage
        # Might not be the best code ever...
        # 10/22/25

        parameters = []
        collectedArguments = 0
        message = ""

        for c in data:
            if c == ':' and collectedArguments < 2:
                collectedArguments += 1

                parameters.append(message)
                message = ""
            else:
                message += c
        
        if collectedArguments < 2:
            raise Exception("Not enough parameters for message! Expected 2 and got " + collectedArguments)
        
        parameters.append(message)

        parameters[0] = parameters[0][1:]
        parameters[len(parameters) - 1] = parameters[len(parameters) - 1].strip()

        if int(parameters[0]) != PROTOCOL_VERSION:
            raise Exception("Debugger message has invalid protocol version, expected: " + PROTOCOL_VERSION + " and got: " + parameters[0])

        self.msg_type = DebuggerMessageType(int(parameters[1]))
        self.parameters = parameters
        self.data = self.parameters[2]
