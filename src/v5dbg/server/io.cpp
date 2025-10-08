#include <iostream>
#include "v5dbg/server.h"

void
V5Dbg_ServerIOMain(v5dbg_server_state_t *pState)
{
  while (pState->canRun)
  {
    std::string cmdBuffer;
    std::getline(std::cin, cmdBuffer);

    V5Dbg_PushMessage(pState, V5Dbg_DeserializeMessage(cmdBuffer));
  }
}
