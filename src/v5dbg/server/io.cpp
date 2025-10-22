#include <exception>
#include <iostream>
#include "v5dbg/server.h"
#include "v5dbg/util.h"

void
V5Dbg_ServerIOMain(v5dbg_server_state_t *pState)
{
  while (pState->canRun)
  {
    std::string cmdBuffer;
    std::getline(std::cin, cmdBuffer);

    try {
      V5Dbg_PushMessage(pState, V5Dbg_DeserializeMessage(cmdBuffer));
    } catch (std::exception &e)
    {
      info("ServerIOReadException: %s", e.what());
    }
  }
}
