#pragma once
#include <memory>
#include "memory.h"

/**
 * Used as the result of a V5Dbg_SetVariable call
 */
enum v5dbg_variable_set_result_e
{
  /// @brief  No pretty printer allocator found
  MEMORY_SET_NO_ALLOCATOR = 0,

  /// @brief  The allocator failed to convert the input string into a raw buffer
  MEMORY_SET_ALLOCATOR_FAILURE = 1,

  /// @brief  Memory set operation completed with no errors and temporary buffers have been freed
  MEMORY_SET_COMPLETE = 2,

  /// @brief  Memory could not be converted to the target type
  MEMORY_SET_CONVERSION_FAILURE = 3
};

/**
 * Dictates the behavior of V5Dbg_SetVariable
 */
enum v5dbg_variable_set_mode_e
{
    /// @brief  Set the memory of this variable once
    VARIABLE_SET_MODE_SINGLE = 0,

    /// @brief  Set the memory of this variable even after its reallocated
    VARIABLE_SET_MODE_CONST = 1
};

/**
 * Handles setting the memory of a given stack variable using the type database
 * @param mem Variable to set the value of
 * @param pSet String to cast and copy into the variable
 * @param mode Variable set mode, faults to VARIABLE_SET_MODE_SINGLE
 * @return v5dbg_variable_set_result_e for the result
 */
v5dbg_variable_set_result_e V5Dbg_SetVariable(const std::shared_ptr<V5DbgMemoryObject> &mem, const std::string &pSet, v5dbg_variable_set_mode_e setMode = VARIABLE_SET_MODE_SINGLE);
