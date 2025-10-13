#include "v5dbg/debinfo.h"
#include "v5dbg/debugger.h"
#include "v5dbg/msg.h"
#include "v5dbg/server.h"
#include "v5dbg/stack.h"

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

  printf("Finding memory for: frame %i on thread %i\n", stackFrame, threadID);

  v5dbg_thread_t* thread = V5Dbg_ThreadWithID(pState, threadID);
  if (thread == nullptr)
  {
    printf("NoThread!\n");
    return;
  }

  for (int i = 0; i < thread->stack.size(); i++)
  {
    printf("%i\n", i);

    if (i == stackFrame)
    {
      printf("Stack mem:\n");

      for (auto& obj : thread->stack[i].pMemory->local)
      {
        printf("(%i) void* ptr = %p\n", obj->getID(), obj->getPtr());
      }

      break;
    }
  }
}
