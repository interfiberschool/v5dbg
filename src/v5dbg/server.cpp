#include "v5dbg/server.h"
#include <iostream>
#include <mutex>
#include <stdio.h>
#include "pros/apix.h" // Kernel API
#include "pros/llemu.hpp"
#include "pros/rtos.h"
#include "pros/rtos.hpp"
#include "protocol.h"
#include "v5dbg/debugger.h"
#include "v5dbg/msg.h"
#include "v5dbg/stack.h"
#include "v5dbg/util.h"

using namespace pros::c;

v5dbg_server_state_t
V5Dbg_AllocateServerState()
{
  v5dbg_server_state_t state{};

  state.threadListLock = new pros::rtos::Mutex();
  state.messageQueueLock = new pros::rtos::Mutex();
  state.canRun = true;

  return state;
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

void
V5Dbg_StartServer(v5dbg_server_state_t* pState)
{
  if (pState == nullptr)
  {
    info("Allocated state is nullptr");
    return;
  }

  info("ServerInit");

  CURRENT_SERVER = pState;

  // Default to serial IO
  if (CURRENT_SERVER->serial == nullptr)
  {
    V5Dbg_SetWriteMode(pState, WRITE_MODE_SERIAL);
  }

  pros::rtos::Task* serverTask
    = new pros::rtos::Task([]() { V5Dbg_ServerMain(); }, TASK_PRIORITY_MAX, TASK_STACK_DEPTH_DEFAULT, "v5dbg Server");

  pState->serverTask = serverTask;
}

v5dbg_thread_t*
V5Dbg_Init()
{
  return V5Dbg_RemoteInit(pros::rtos::Task::current());
}

void
V5Dbg_Leave(v5dbg_thread_t* pThread)
{
  std::lock_guard<pros::rtos::Mutex> _g(*CURRENT_SERVER->threadListLock);

  for (int i = 0; i < CURRENT_SERVER->threads.size(); i++)
  {
    if (CURRENT_SERVER->threads[i].name == pThread->name)
    {
      CURRENT_SERVER->threads.erase(CURRENT_SERVER->threads.begin() + i);
      return;
    }
  }
}

v5dbg_thread_t*
V5Dbg_RemoteInit(pros::rtos::Task other)
{
  info("RemoteInit");

  std::lock_guard<pros::rtos::Mutex> _g(*CURRENT_SERVER->threadListLock);

  v5dbg_thread_t thread = V5Dbg_AllocateServerThread();
  thread.task = other;
  thread.name = other.get_name();
  thread.threadLock = new pros::rtos::Mutex();

  CURRENT_SERVER->threads.push_back(thread);

  info("RemoteInitDone");

  return &CURRENT_SERVER->threads.back();
}

v5dbg_thread_t
V5Dbg_AllocateServerThread()
{
  v5dbg_thread_t thread{};
  thread.threadLock = new pros::rtos::Mutex();

  return thread;
}

void
V5Dbg_ServerMain()
{
  CURRENT_SERVER->ioTask = new pros::rtos::Task([]() { V5Dbg_ServerIOMain(CURRENT_SERVER); }, TASK_PRIORITY_MAX,
                                                TASK_STACK_DEPTH_DEFAULT, "v5dbg IO server");

  // Configure message handler list
  V5Dbg_PrimeServerMessageHandlers(CURRENT_SERVER);

  v5dbg_message_t open{};
  open.type = DEBUGGER_MESSAGE_OPEN;
  open.paramBuffer = "SERVEROPEN";

  V5Dbg_WriteToOut(V5Dbg_SerializeMessage(open));

  // Send an OPEN message to the debugger every once and awhile incase we miss the first one somehow
  pros::rtos::Task openPoll(
    []()
    {
      while (true)
      {
        v5dbg_message_t open{};
        open.type = DEBUGGER_MESSAGE_OPEN;
        open.paramBuffer = "SERVEROPEN";

        V5Dbg_WriteToOut(V5Dbg_SerializeMessage(open));

        pros::delay(2000);
      }
    });

  while (CURRENT_SERVER->canRun)
  {
    if (!V5Dbg_CanPump(CURRENT_SERVER))
    {
      pros::delay(10);
      continue;
    }


    try
    {
      const v5dbg_message_t message = V5Dbg_NextMessage(CURRENT_SERVER);

      bool f = false;

      for (auto& handler : CURRENT_SERVER->messageHandlers)
      {
        if (handler.messageType == message.type)
        {
          handler.handler(CURRENT_SERVER, message);
          f = true;

          break;
        }
      }

      if (!f)
      {
        info("Invalid message with type: %i", message.type);
      }
    }
    catch (std::exception& e)
    {
      info("MessageHandlerException: %s", e.what());
    }

    // Debugger delay of 10ms
    pros::delay(10);
  }
}

v5dbg_thread_t*
V5Dbg_ThreadForTask()
{
  return V5Dbg_ThreadForTask(CURRENT_SERVER);
}

v5dbg_thread_t*
V5Dbg_ThreadForTask(v5dbg_server_state_t* pState)
{
  std::lock_guard<pros::rtos::Mutex> _g(*pState->threadListLock);

  for (auto& task : pState->threads)
  {
    if (task.task.get_name() == pros::rtos::Task::current().get_name())
    {
      return &task;
    }
  }


  return nullptr;
}

v5dbg_thread_t*
V5Dbg_ThreadWithID(v5dbg_server_state_t* pState, int id)
{
  std::lock_guard<pros::rtos::Mutex> _g(*pState->threadListLock);

  for (int i = 0; i < pState->threads.size(); i++)
  {
    if (i == id)
    {
      return &pState->threads[i];
    }
  }

  return nullptr;
}

v5dbg_thread_t*
V5Dbg_ThreadWithID(int id)
{
  return V5Dbg_ThreadWithID(id);
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
