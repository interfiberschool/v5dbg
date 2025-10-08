#include <mutex>
#include "v5dbg/server.h"

bool
V5Dbg_CanPump(const v5dbg_server_state_t *pState)
{
  return !pState->messageQueue.empty();
}

v5dbg_message_t
V5Dbg_NextMessage(v5dbg_server_state_t *pState)
{
  std::lock_guard<pros::rtos::Mutex> _g(*pState->messageQueueLock);

  const v5dbg_message_t msg = pState->messageQueue.back();

  pState->messageQueue.pop();

  return msg;
}

void
V5Dbg_PushMessage(v5dbg_server_state_t *pState, const v5dbg_message_t& msg)
{
  std::lock_guard<pros::rtos::Mutex> _g(*pState->messageQueueLock);

  pState->messageQueue.push(msg);
}
