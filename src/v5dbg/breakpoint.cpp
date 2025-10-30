#include "v5dbg/breakpoint.h"
#include "debinfo.h"
#include "debugger.h"
#include "protocol.h"
#include "server.h"
#include "util.h"


void
V5Dbg_BreakpointMain(v5dbg_server_state_t* pState, v5dbg_breakpoint_t* breakpoint)
{
  if (!breakpoint->enabled)
    return;

  v5dbg_message_t msg{};
  msg.type = DEBUGGER_MESSAGE_BREAK_INVOKED;
  msg.paramBuffer = V5Dbg_FormatPrint("%i:[%s]:%s:%i", breakpoint->id, breakpoint->location.functionName.c_str(),
                                      breakpoint->location.filePath.c_str(), breakpoint->location.lineNumber);

  V5Dbg_WriteToOut(V5Dbg_SerializeMessage(msg));

  // Force reset justAwoke state
  pState->justAwoke = false;

  // Emulate suspend message and wait for the program to resume execution
  v5dbg_message_t suspend{};
  suspend.type = DEBUGGER_MESSAGE_SUSPEND;

  V5Dbg_PushMessage(pState, suspend);

  V5Dbg_WaitForSuspend(V5Dbg_GetCurrentServer());
}

v5dbg_breakpoint_t*
V5Dbg_Breakpoint(bool enabled, const v5dbg_code_point_t& loc)
{
  v5dbg_breakpoint_t* b = new v5dbg_breakpoint_t{};
  b->enabled = enabled;
  b->location = loc;

  b->id = V5Dbg_GetBreakpointManager()->nextID++;

  V5Dbg_GetBreakpointManager()->breakpoints.push_back(b);

  return b;
}
