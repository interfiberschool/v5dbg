#include "v5dbg/server.h"
#include <iostream>
#include <mutex>
#include "pros/rtos.h"
#include "v5dbg/debugger.h"
#include "v5dbg/msg.h"
#include "v5dbg/stack.h"

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
V5Dbg_StartServer(v5dbg_server_state_t* pState)
{
  if (pState == nullptr)
  {
    printf("Allocated state is nullptr\n");
    return;
  }

  printf("ServerInit\n");

  CURRENT_SERVER = pState;

  pros::rtos::Task* serverTask
    = new pros::rtos::Task([]() { V5Dbg_ServerMain(); }, TASK_PRIORITY_MAX, TASK_STACK_DEPTH_DEFAULT, "v5dbg Server");

  pState->serverTask = serverTask;
}

v5dbg_thread_t*
V5Dbg_Init()
{
  return V5Dbg_RemoteInit(pros::rtos::Task::current());
}

v5dbg_thread_t*
V5Dbg_RemoteInit(pros::rtos::Task other)
{
  printf("RemoteInit\n");

  std::lock_guard<pros::rtos::Mutex> _g(*CURRENT_SERVER->threadListLock);

  v5dbg_thread_t thread = V5Dbg_AllocateServerThread();
  thread.task = other;
  thread.name = other.get_name();
  thread.threadLock = new pros::rtos::Mutex();

  CURRENT_SERVER->threads.push_back(thread);

  printf("RemoteInitDone\n");

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

  while (CURRENT_SERVER->canRun)
  {
    if (!V5Dbg_CanPump(CURRENT_SERVER))
    {
      pros::delay(10);
      continue;
    }

    const v5dbg_message_t message = V5Dbg_NextMessage(CURRENT_SERVER);

    try
    {
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
        printf("Invalid message with type: %i\n", message.type);
      }
    }
    catch (std::exception& e)
    {
      printf("MessageHandlerException: %s\n", e.what());
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
