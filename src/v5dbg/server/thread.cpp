#include "v5dbg/server.h"
#include "pros/rtos.hpp"

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