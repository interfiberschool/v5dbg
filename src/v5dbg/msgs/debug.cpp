#include "v5dbg/msg.h"

// Thread and stack manipulation

void
V5Dbg_ThreadListHandle(v5dbg_server_state_t* pState, const v5dbg_message_t& msg)
{
  v5dbg_message_t rVal{};
  rVal.type = DEBUGGER_MESSAGE_RTHREADS;

  int i = 0;
  for (auto& thread : pState->threads)
  {
    rVal.paramBuffer
      += thread.name + "," + std::to_string(i) + (i + 1 < (int)pState->threads.size() ? "," : "");

    i++;
  }

  printf("%s\n", V5Dbg_SerializeMessage(rVal).c_str());
}

void
V5Dbg_VStackForHandle(v5dbg_server_state_t* pState, const v5dbg_message_t& msg)
{
  v5dbg_message_t rVal{};
  rVal.type = DEBUGGER_MESSAGE_RVSTACK;

  if (msg.paramBuffer.empty())
    return;

  int threadID = std::stoi(msg.paramBuffer);

  int x = 0;
  for (auto& thread : pState->threads)
  {
    // Thread ID match
    if (x == threadID)
    {
      rVal.type = DEBUGGER_MESSAGE_RVSTACK;

      int frameIndex = thread.stack.size() - 1;

      // Generate each line of stack trace;
      for (auto& frame : thread.stack)
      {
        rVal.paramBuffer = "(" + std::to_string(frameIndex) + ") " + frame.funcName + " at " + frame.stackBegin.filePath
          + ":" + std::to_string(frame.stackBegin.lineNumber) + " -> 0x" + std::to_string((uintptr_t)frame.jmpAddress);

        printf("%s\n", V5Dbg_SerializeMessage(rVal).c_str());

        frameIndex--;
      }

      break;


      // End of stack

      rVal.paramBuffer.clear();
      rVal.type = DEBUGGER_MESSAGE_VSTACK_END;

      printf("%s\n", V5Dbg_SerializeMessage(rVal).c_str());
    }

    x++;
  }
}
