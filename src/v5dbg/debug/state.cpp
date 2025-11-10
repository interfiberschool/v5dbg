#include "v5dbg/state.h"
#include <mutex>
#include "pros/rtos.hpp"
#include "util.h"
#include "v5dbg/server.h"
#include "v5dbg/stack.h"

void
V5Dbg_SuspendProgram(v5dbg_server_state_t* pState)
{
  std::lock_guard<pros::rtos::Mutex> g(*pState->threadListLock);

  for (auto& task : pState->threads)
  {
    task.task.suspend();
  }

  pState->justAwoke = false;

  info("Program suspended");
}

void
V5Dbg_ResumeProgram(v5dbg_server_state_t* pState)
{
  std::lock_guard<pros::rtos::Mutex> g(*pState->threadListLock);

  for (auto& task : pState->threads)
  {
    if (task.task.get_state() & pros::E_TASK_STATE_SUSPENDED)
    {
      task.task.resume();
    }
  }

  pState->justAwoke = true;

  info("Program resumed\n");
}

void
V5Dbg_WaitForSuspend(v5dbg_server_state_t *pState)
{
  // Wait for program to enter suspend state

  while (!pState->justAwoke)
  {
    info_pre("Waiting for resume...");
    pros::delay(50);
  }
}
