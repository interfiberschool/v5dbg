#pragma once
#include "v5dbg/server.h"
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
  bool enabled = true;
};

/// @brief  Manage a breakpoint, should only be called by the $break macro
void V5Dbg_BreakpointMain(v5dbg_server_state_t *pState, v5dbg_breakpoint_t *breakpoint);