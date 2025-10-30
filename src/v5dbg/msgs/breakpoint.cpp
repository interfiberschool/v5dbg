#include "v5dbg/breakpoint.h"
#include "v5dbg/msg.h"
#include "v5dbg/protocol.h"
#include "v5dbg/server.h"
#include "v5dbg/util.h"

void
V5Dbg_LBreakpointsHandle(v5dbg_server_state_t* pState, const v5dbg_message_t& msg)
{
    v5dbg_message_t rVal{};
    rVal.type = DEBUGGER_MESSAGE_RBREAKPOINT;

    for (auto &breakpoint : V5Dbg_GetBreakpointManager()->breakpoints)
    {
        rVal.paramBuffer = V5Dbg_FormatPrint("%i:[%s]:%s:%i", breakpoint.id, breakpoint.location.functionName.c_str(), breakpoint.location.filePath.c_str(), breakpoint.location.lineNumber);

        V5Dbg_WriteToOut(V5Dbg_SerializeMessage(rVal));
    }

    rVal.paramBuffer = "ENDBREAKS";
    rVal.type = DEBUGGER_MESSAGE_END_BREAKPOINTS;

    V5Dbg_WriteToOut(V5Dbg_SerializeMessage(rVal));
}
