#include "v5dbg/set.h"
#include "pretty.h"

bool V5Dbg_SetVariable(const std::shared_ptr<V5DbgMemoryObject> &mem, const std::string &pSet)
{
  v5dbg_pretty_printer_state_t *state = V5Dbg_GetPrettyPrinterState();

  // Find our buffer allocator we should use
  for (auto &alloc : state->allocators)
  {
    if (alloc.first == mem->getMemoryType())
    {
      // Found our buffer allocator, now we can invoke it to allocate our memory

      void* buffer = alloc.second(mem.get(), pSet);

      if (buffer == nullptr)
      {
        info("Buffer allocation failed!");
        break;
      }

      mem->setBuffer(buffer);

      free(buffer);

      return true;
    }
  }

  info("Variable set failed due to no valid buffer allocator found");

  return false;
}