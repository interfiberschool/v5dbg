#pragma once
#include "v5dbg/debinfo.h"
#include "v5dbg/server.h"
#include "v5dbg/stack.h"
#include "v5dbg/breakpoint.h"

/*
 * Main user-facing API
 */

class V5DbgAutoTask
{
public:
  V5DbgAutoTask() { m_thread = V5Dbg_Init(); }

  ~V5DbgAutoTask()
  {
    V5Dbg_Leave(m_thread);
  }

private:
  v5dbg_thread_t *m_thread;
};

/**
 * Begin a debuggable function
 * @note Without this your function will not appear in stack traces and most debugger functions will not work
 */
#define $function                                                                                                      \
  __v5dbg_func:                                                                                                        \
  static V5DbgStackMemory _v5dbg_stack_func_memory;                                                                                      \
  V5DbgFunction _v5dbg_stack_func(__PRETTY_FUNCTION__, __FILE__, __LINE__, &&__v5dbg_func, &_v5dbg_stack_func_memory); \
  v5dbg_breakpoint_t *_v5dbg_break_c = nullptr; \

/**
 * @brief  Expose a scoped variable to the debugger.
 * @note Can only be called within a debuggable function
 */
#define $expose(target)                                                                                                \
  constexpr int _v5dbg_var_line_##target = __LINE__; \
  static v5dbg_variable_t _v5dbg_var_info_##target{}; \
  if (_v5dbg_var_info_##target.name.empty()) { \
  _v5dbg_var_info_##target.name = #target; \
  _v5dbg_var_info_##target.typeName = V5Dbg_Demangle(typeid(target).name());\
  _v5dbg_var_info_##target.allocationPoint.filePath = __FILE__; \
  _v5dbg_var_info_##target.allocationPoint.lineNumber = _v5dbg_var_line_##target; \
  } \
  static std::shared_ptr<V5DbgMemoryObject> _v5dbg_var_##target = std::make_shared<V5DbgMemoryObject>(_v5dbg_var_info_##target);               \
  _v5dbg_var_##target->setMemoryType(V5Dbg_MemoryTypeFromType(typeid(target))); \
  _v5dbg_var_##target->setPtr(&target);                                                                                \
  _v5dbg_stack_func.expose(_v5dbg_var_##target);

/// @brief Disabled by default breakpoint
#define $break { static v5dbg_breakpoint_t* _v5dbg_break_c = V5Dbg_Breakpoint(false, { .filePath = __FILE__, .lineNumber = __LINE__, .functionName = __PRETTY_FUNCTION__ }); \
    V5Dbg_BreakpointMain(V5Dbg_GetCurrentServer(), _v5dbg_break_c); \
  }

#define $ntask V5DbgAutoTask _v5dbg_ctask;