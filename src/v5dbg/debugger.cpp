#include "v5dbg/debugger.h"
#include <mutex>
#include "pros/rtos.hpp"
#include "util.h"
#include "v5dbg/server.h"
#include "v5dbg/stack.h"

void
V5Dbg_SuspendProgram(v5dbg_server_state_t* pState)
{
  std::lock_guard<pros::rtos::Mutex> g(*pState->threadListLock);

  info("SuspendState: %p", pState);

  for (auto& task : pState->threads)
  {
    task.task.suspend();
  }

  pState->justAwoke = false;

  info("ProgramSuspend");
}

void
V5Dbg_ResumeProgram(v5dbg_server_state_t* pState)
{
  std::lock_guard<pros::rtos::Mutex> g(*pState->threadListLock);

  info("ResumeState: %p\n", pState);

  for (auto& task : pState->threads)
  {
    if (task.task.get_state() & pros::E_TASK_STATE_SUSPENDED)
    {
      task.task.resume();
    }
  }

  pState->justAwoke = true;

  info("ProgramResume\n");
}
