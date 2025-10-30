#pragma once
#include "v5dbg/server.h"
#include "v5dbg/debinfo.h"
#include <cstdint>
#include <map>
#include <functional>

/// @brief  Debugger breakpoint
struct v5dbg_breakpoint_t
{
  /// @brief  Breakpoint ID
  uint32_t id = 0;

  /// @brief  Location where the breakpoint has been placed
  v5dbg_code_point_t location{};

  /// @brief  (Optional) conditional breakpoint trigger
  std::function<bool()> cond;

  /// @brief  Will this breakpoint be invoked when it's hit?
  bool enabled = true;
};

/// @brief  Global breakpoint manager
struct v5dbg_breakpoint_manager_t
{
  /// @brief  Breakpoint ID
  uint32_t nextID = 0;

  /// @brief  Registered breakpoints
  std::vector<v5dbg_breakpoint_t*> breakpoints;
};

/// @brief  Return the global breakpoint manager instance
inline v5dbg_breakpoint_manager_t* V5Dbg_GetBreakpointManager()
{
  static v5dbg_breakpoint_manager_t mgr{};
  return &mgr;
}

/// @brief  Allocate or get a breakpoint at the given location
v5dbg_breakpoint_t V5Dbg_Breakpoint(bool enabled, const v5dbg_code_point_t &loc);

/// @brief  Manage a breakpoint, should only be called by the $break macro
void V5Dbg_BreakpointMain(v5dbg_server_state_t *pState, v5dbg_breakpoint_t *breakpoint);