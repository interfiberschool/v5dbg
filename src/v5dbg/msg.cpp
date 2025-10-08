#include "v5dbg/msg.h"
#include <mutex>
#include "pros/rtos.hpp"

void
V5Dbg_AddServerMessageHandler(v5dbg_server_state_t* pState, v5dbg_server_msg_callback_t callback)
{
  pState->messageHandlers.push_back(std::move(callback));
}

void V5Dbg_PrimeServerMessageHandlers(v5dbg_server_state_t *pState) {
  V5Dbg_AddServerMessageHandler(pState, {
    .messageType = DEBUGGER_MESSAGE_SUSPEND,
    .handler = V5Dbg_ServerSuspendHandle,
  });

  V5Dbg_AddServerMessageHandler(pState, {
    .messageType = DEBUGGER_MESSAGE_ALLOCATE_STRING,
    .handler = V5Dbg_AllocateStringHandle,
  });

  V5Dbg_AddServerMessageHandler(pState, {
    .messageType = DEBUGGER_MESSAGE_RESUME,
    .handler = V5Dbg_ServerResumeHandle
  });

  V5Dbg_AddServerMessageHandler(pState, {
    .messageType = DEBUGGER_MESSAGE_THREADS,
    .handler = V5Dbg_ThreadListHandle
  });

  V5Dbg_AddServerMessageHandler(pState, {
    .messageType = DEBUGGER_MESSAGE_VSTACK_FOR,
    .handler = V5Dbg_VStackForHandle
  });
}