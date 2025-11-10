#include <mutex>
#include "v5dbg/debinfo.h"
#include "v5dbg/server.h"
#include "pros/rtos.hpp"
#include "v5dbg/stack.h"

v5dbg_thread_t*
V5Dbg_Init()
{
  return V5Dbg_RemoteInit(pros::rtos::Task::current());
}

void
V5Dbg_Leave(v5dbg_thread_t* pThread)
{
  std::lock_guard<pros::rtos::Mutex> _g(*V5Dbg_GetCurrentServer()->threadListLock);

  for (int i = 0; i < V5Dbg_GetCurrentServer()->threads.size(); i++)
  {
    if (V5Dbg_GetCurrentServer()->threads[i].name == pThread->name)
    {
      V5Dbg_GetCurrentServer()->threads.erase(V5Dbg_GetCurrentServer()->threads.begin() + i);
      return;
    }
  }
}

v5dbg_thread_t*
V5Dbg_RemoteInit(pros::rtos::Task other)
{
  info("RemoteInit");

  std::lock_guard<pros::rtos::Mutex> _g(*V5Dbg_GetCurrentServer()->threadListLock);

  v5dbg_thread_t thread = V5Dbg_AllocateServerThread();
  thread.task = other;
  thread.name = other.get_name();
  thread.threadLock = new pros::rtos::Mutex();

  V5Dbg_GetCurrentServer()->threads.push_back(thread);

  info("RemoteInitDone");

  return &V5Dbg_GetCurrentServer()->threads.back();
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

v5dbg_thread_t*
V5Dbg_ThreadForTask()
{
  return V5Dbg_ThreadForTask(V5Dbg_GetCurrentServer());
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