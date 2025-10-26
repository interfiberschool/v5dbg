#include "v5dbg/debinfo.h"
#include "v5dbg/debugger.h"
#include "v5dbg/msg.h"
#include "v5dbg/pretty.h"
#include "v5dbg/protocol.h"
#include "v5dbg/server.h"
#include "v5dbg/stack.h"
#include "v5dbg/util.h"

void
V5Dbg_LMemForHandle(v5dbg_server_state_t* pState, const v5dbg_message_t& msg)
{
  int stackFrame = -1;
  int threadID = -1;

  int x = 0;
  std::string collect;

  for (char c : msg.paramBuffer)
  {
    if (c == ',' && x == 0)
    {
      stackFrame = std::stoi(collect);
      collect.clear();
      x = 1;

      continue;
    }
    else if (c == ',')
    {
      continue;
    }

    collect += c;
  }

  if (x == 1)
  {
    threadID = std::stoi(collect);
  }

  v5dbg_thread_t* thread = V5Dbg_ThreadWithID(pState, threadID);
  if (thread == nullptr)
  {
    info("NoThread");
    return;
  }

  v5dbg_message_t result{};
  result.type = DEBUGGER_MESSAGE_RLMEM;

  int stackID = thread->stack.size() - 1;
  for (int i = 0; i < thread->stack.size(); i++)
  {
    if (stackID == stackFrame)
    {
      for (auto& obj : thread->stack[i].pMemory->local)
      {
        v5dbg_code_point_t cPoint = obj->getVariable().allocationPoint;

        v5dbg_pretty_printed_t prettyPrint = V5Dbg_PrettyPrint(obj.get());

        // type name, variable name, pretty printed string buffer
        result.paramBuffer = V5Dbg_FormatPrint("[%s]:%s", prettyPrint.typeName.c_str(), prettyPrint.varName.c_str());

        // debug info location
        result.paramBuffer += V5Dbg_FormatPrint(":%s:%i:[%s]", cPoint.filePath.c_str(), cPoint.lineNumber, prettyPrint.printBuffer.c_str());

        V5Dbg_WriteToOut(V5Dbg_SerializeMessage(result));
      }

      break;
    }

    stackID--;
  }

  result.paramBuffer = "ENDSTACKMEM";
  result.type = DEBUGGER_MESSAGE_LMEM_END;

  V5Dbg_WriteToOut(V5Dbg_SerializeMessage(result));
}
