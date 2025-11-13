from server.protocol import PROTOCOL_VERSION
"""
Global debugger configuration
"""
class DebuggerConfig:
    NAME = "V5 Debugger"
    VERSION = "v0.2"

    @staticmethod
    def left() -> str:
        return f'{DebuggerConfig.NAME} {DebuggerConfig.VERSION} (Protocol {PROTOCOL_VERSION})'
