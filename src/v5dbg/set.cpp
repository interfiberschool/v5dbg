#include "v5dbg/set.h"
#include "pretty.h"

v5dbg_variable_set_result_e V5Dbg_SetVariable(const std::shared_ptr<V5DbgMemoryObject> &mem, const std::string &pSet)
{
  v5dbg_pretty_printer_state_t *state = V5Dbg_GetPrettyPrinterState();

  // Find our buffer allocator we should use
  for (auto &alloc : state->allocators)
  {
    if (alloc.first == mem->getMemoryType())
    {
      // Found our buffer allocator, now we can invoke it to allocate our memory

      void* buffer = alloc.second(pSet); // Allocate our buffer!

      if (buffer == nullptr)
        return MEMORY_SET_ALLOCATOR_FAILURE;

      mem->setBuffer(buffer);

      free(buffer);

      return MEMORY_SET_COMPLETE;
    }
  }

  return MEMORY_SET_NO_ALLOCATOR;
}