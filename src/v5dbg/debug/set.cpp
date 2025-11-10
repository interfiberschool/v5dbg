#include "v5dbg/set.h"
#include "v5dbg/pretty.h"

v5dbg_variable_set_result_e V5Dbg_SetVariable(const std::shared_ptr<V5DbgMemoryObject> &mem, const std::string &pSet, v5dbg_variable_set_mode_e setMode)
{
  v5dbg_pretty_printer_state_t *state = V5Dbg_GetPrettyPrinterState();

  // Find our buffer allocator we should use
  for (auto &alloc : state->allocators)
  {
    if (alloc.first == mem->getMemoryType())
    {
      // Found our buffer allocator, now we can invoke it to allocate our memory

      void* buffer = alloc.second(pSet); // Allocate our buffer!

      if (buffer == nullptr) // We failed to convert the input data to the target data type
        return MEMORY_SET_CONVERSION_FAILURE;

      if (!mem->setBuffer(buffer))
      {
        // Something failed with our memcpy operation! Free our temp buffer and move on...

        free(buffer);

        return MEMORY_SET_ALLOCATOR_FAILURE;
      }

      // When in const mode we set the recopy buffer
      // otherwise we just free our buffer.
      // When setRecopyBuffer is called the previous recopy buffer is deallocated

      if (setMode == VARIABLE_SET_MODE_SINGLE)
      {
         free(buffer);
      }
      else if (setMode == VARIABLE_SET_MODE_CONST)
      {
          mem->setRecopyBuffer(buffer);
      }

      // Our memory set operation was a success!
      return MEMORY_SET_COMPLETE;
    }
  }

  return MEMORY_SET_NO_ALLOCATOR;
}
