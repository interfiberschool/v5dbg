#include "v5dbg/stack.h"
#include <mutex>
#include "memory.h"
#include "stack.h"
#include "v5dbg/debinfo.h"
#include "v5dbg/server.h"

V5DbgFunction::V5DbgFunction(const std::string& name, const char* file, int line, void* pAddress,
                             V5DbgStackMemory* memory)
{
  v5dbg_thread_t* thread = V5Dbg_ThreadForTask();
  if (thread == nullptr)
  {
    return;
  }

  m_memory = memory;

  std::lock_guard<pros::rtos::Mutex> _g(*thread->threadLock);

  v5dbg_stack_frame_t frame{};
  frame.funcName = name;
  frame.jmpAddress = pAddress;
  frame.stackBegin.filePath = file;
  frame.stackBegin.lineNumber = line;
  frame.pMemory = m_memory->getMemory(); // Pointer is only valid until object destruction and stack pop

  thread->stack.push_back(frame);
}

void
V5DbgFunction::expose(const std::shared_ptr<V5DbgMemoryObject>& memObject)
{
  m_memory->expose(memObject);
}

V5DbgFunction::~V5DbgFunction()
{
  v5dbg_thread_t* thread = V5Dbg_ThreadForTask();
  if (thread == nullptr)
  {
    return;
  }

  thread->stack.pop_back();

  // Deallocate
  m_memory->deallocateAll();

  // When the program is paused before a stack pop we can inspect each threads
  // virtual stack in order to determine the current execution location down to
  // the function
}


void
V5DbgStackMemory::expose(const std::shared_ptr<V5DbgMemoryObject>& obj)
{
  for (auto &v : m_memory.local)
  {
    if (v->getID() == obj->getID())
    {
      printf("Overwriting old stack memory info!\n");

      v->setPtr(obj->getPtr());
      v->memState = MEMORY_STATE_ALLOCATED;

      return;
    }
  }

  m_memory.local.push_back(obj);
}

void V5DbgStackMemory::deallocateAll()
{
  for (auto &obj : m_memory.local)
  {
    obj->setPtr(nullptr);
    obj->memState = MEMORY_STATE_DEALLOCATED;
  }
}