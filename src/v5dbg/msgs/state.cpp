#include "v5dbg/debugger.h"
#include "v5dbg/msg.h"

// Program state manipulation

void
V5Dbg_ServerSuspendHandle(v5dbg_server_state_t* pState, const v5dbg_message_t& msg)
{
  V5Dbg_SuspendProgram(pState);
}

void
V5Dbg_ServerResumeHandle(v5dbg_server_state_t* pState, const v5dbg_message_t& msg)
{
  V5Dbg_ResumeProgram(pState);
}

void
V5Dbg_AllocateStringHandle(v5dbg_server_state_t* pState, const v5dbg_message_t& msg)
{
  printf("%s\n", V5Dbg_SerializeMessage(msg).c_str());
}