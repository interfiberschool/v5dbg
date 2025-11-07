#pragma once
#include <memory>
#include "memory.h"

enum v5dbg_variable_set_result_e
{
  /// @brief  No pretty printer allocator found
  MEMORY_SET_NO_ALLOCATOR = 0,

  /// @brief  The allocator failed to convert the input string into a raw buffer
  MEMORY_SET_ALLOCATOR_FAILURE = 1,

  /// @brief  Memory set operation completed with no errors and temporary buffers have been freed
  MEMORY_SET_COMPLETE = 2
};


/**
 * Handles setting the memory of a given stack variable using the type database
 * @param mem Variable to set the value of
 * @param pSet String to cast and copy into the variable
 * @return v5dbg_variable_set_result_e for the result
 */
v5dbg_variable_set_result_e V5Dbg_SetVariable(const std::shared_ptr<V5DbgMemoryObject> &mem, const std::string &pSet);