#pragma once
#include "v5dbg/debinfo.h"
#include <functional>

/// @brief  Debugger breakpoint
struct v5dbg_breakpoint_t
{
  /// @brief  Location where the breakpoint has been placed
  v5dbg_code_point_t location;

  /// @brief  (Optional) conditional breakpoint trigger
  std::function<bool()> cond;

  /// @brief  Will this breakpoint be invoked when it's hit?
  bool enabled = false;
};

/**
 * Add a breakpoint to the debug server
 * @param Pointer to breakpoint information in memory, should be statically allocated
 */
void V5Dbg_AddBreak(v5dbg_breakpoint_t *breakpoint);

/// @brief  Invoke a breakpoint if its been enabled & its condition is true
void V5Dbg_InvokeBreak(v5dbg_breakpoint_t *breakpoint);