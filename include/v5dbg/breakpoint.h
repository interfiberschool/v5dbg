#pragma once
#include "v5dbg/server.h"
#include "v5dbg/debinfo.h"
#include <cstdint>
#include <functional>

enum v5dbg_breakpoint_type_e
{
  /// @brief  Static breakpoint which trips when its enabled
  BREAKPOINT_STATIC = 0,

  /// @brief  Breakpoint which trips when its enabled and its condition evalulates to true
  BREAKPOINT_CONDITIONAL = 1
};

/// @brief  Debugger breakpoint
struct v5dbg_breakpoint_t
{
  /// @brief  Custom breakpoint name appended after the function name like `void main()+alloc:x`
  std::string name;

  /// @brief  Breakpoint type
  v5dbg_breakpoint_type_e type;

  /// @brief  Breakpoint ID
  uint32_t id = 0;

  /// @brief  Location where the breakpoint has been placed
  v5dbg_code_point_t location{};

  /// @brief  (Optional) conditional breakpoint trigger
  std::function<bool()> cond;

  /// @brief  Will this breakpoint be invoked when it's hit?
  bool enabled = true;

  /// @brief  Will this breakpoint show up in a breakpoint listing, usually enabled for allocation breakpoints
  bool hidden = false;
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
v5dbg_breakpoint_t* V5Dbg_Breakpoint(bool enabled, const v5dbg_code_point_t &loc);

/// @brief  Allocate or get a breakpoint at the given location (conditional)
v5dbg_breakpoint_t* V5Dbg_BreakpointCond(bool enabled, const v5dbg_code_point_t &loc, const std::function<bool()> &cond);

/// @brief  Manage a breakpoint, should only be called by the $break macro
void V5Dbg_BreakpointMain(v5dbg_server_state_t *pState, const v5dbg_breakpoint_t *breakpoint);