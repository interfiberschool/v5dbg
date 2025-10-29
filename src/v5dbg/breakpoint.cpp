#include "v5dbg/breakpoint.h"
#include "debugger.h"
#include "protocol.h"
#include "server.h"


void 
V5Dbg_BreakpointMain(v5dbg_server_state_t *pState, v5dbg_breakpoint_t *breakpoint)
{
  if (!breakpoint->enabled) return;
  breakpoint->enabled = false;

  v5dbg_message_t msg{};
  msg.type = DEBUGGER_MESSAGE_BREAK_INVOKED;
  msg.paramBuffer = "todo";

  V5Dbg_WriteToOut(V5Dbg_SerializeMessage(msg));

  // Force reset justAwoke state
  pState->justAwoke = false;

  // Emulate suspend message and wait for the program to resume execution
  v5dbg_message_t suspend{};
  suspend.type = DEBUGGER_MESSAGE_SUSPEND;

  V5Dbg_PushMessage(pState, suspend);

  V5Dbg_WaitForSuspend(V5Dbg_GetCurrentServer());
}