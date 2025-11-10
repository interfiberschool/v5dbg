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

void
V5Dbg_SetWriteMode(v5dbg_server_state_t* pState, v5dbg_server_write_mode_e writeMode)
{
  if (writeMode == WRITE_MODE_SERIAL)
  {
    pState->serial = fopen("/ser/sout", "wb");

    if (pState->serial == nullptr)
    {
      info("Failed to open /ser/sout for serial comms!");
    }

    // Disables COBS when writing to stdout, makes reading data on the debugger end much simpler
    serctl(SERCTL_DISABLE_COBS, nullptr);
  }
}

void
V5Dbg_WriteToOut(const std::string& msg)
{
  // This function used to handle writing to the actual serial device file but disabling COBS for all write operations
  // seems to be better and it replaces fwrite/fflush with printf
  if (CURRENT_SERVER == nullptr)
  {
    info("V5Dbg_WriteToOut(...): Must have a server allocated!");
    return;
  }

  if (CURRENT_SERVER->serial == nullptr)
  {
    info("V5Dbg_WriteToOut(...): V5Dbg_SetWriteMode(...) was never called, or failed!");
  }

  std::string buf = msg + "\n";

  fwrite(buf.c_str(), buf.size(), 1, CURRENT_SERVER->serial);
}