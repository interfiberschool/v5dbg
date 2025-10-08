#pragma once
#include "v5dbg/stack.h"

/*
 * Main user-facing API
 */

/// @brief  Begin a debuggable function
#define $function                                                                                                      \
  __v5dbg_func:                                                                                                        \
  V5DbgFunction _fStackCatch(__PRETTY_FUNCTION__, __FILE__, __LINE__, &&__v5dbg_func);
