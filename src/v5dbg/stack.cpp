#include "v5dbg/stack.h"
#include "v5dbg/debinfo.h"
#include <mutex>
#include "v5dbg/server.h"

V5DbgFunction::V5DbgFunction(const std::string& name, const char* file, int line, void* pAddress)
{
  v5dbg_thread_t* thread = V5Dbg_ThreadForTask();
  if (thread == nullptr)
  {
    return;
  }

  std::lock_guard<pros::rtos::Mutex> _g(*thread->threadLock);

  v5dbg_stack_frame_t frame{};
  frame.funcName = name;
  frame.jmpAddress = pAddress;
  frame.stackBegin.filePath = file;
  frame.stackBegin.lineNumber = line;

  thread->stack.push_back(frame);
}

V5DbgFunction::~V5DbgFunction()
{
  v5dbg_thread_t* thread = V5Dbg_ThreadForTask();
  if (thread == nullptr)
  {
    return;
  }

  thread->stack.pop_back();

  // When the program is paused before a stack pop we can inspect each threads
  // virtual stack in order to determine the current execution location down to
  // the function
}
