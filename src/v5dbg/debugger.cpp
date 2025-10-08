#include "v5dbg/debugger.h"
#include <mutex>
#include "pros/rtos.hpp"
#include "v5dbg/server.h"
#include "v5dbg/stack.h"

void
V5Dbg_SuspendProgram(v5dbg_server_state_t* pState)
{
  std::lock_guard<pros::rtos::Mutex> g(*pState->threadListLock);

  printf("SuspendState: %p\n", pState);

  for (auto& task : pState->threads)
  {
    task.task.suspend();
  }

  printf("ProgramSuspend\n");
}

void
V5Dbg_ResumeProgram(v5dbg_server_state_t* pState)
{
  std::lock_guard<pros::rtos::Mutex> g(*pState->threadListLock);

  printf("ResumeState: %p\n", pState);

  for (auto& task : pState->threads)
  {
    if (task.task.get_state() & pros::E_TASK_STATE_SUSPENDED)
    {
      task.task.resume();
    }
  }

  printf("ProgramResume\n");
}
