#pragma once

struct v5dbg_server_state_t;

/// @brief  Suspend the running program until V5Dbg_ResumeProgram(...) is called
void V5Dbg_SuspendProgram(v5dbg_server_state_t* pState);

/// @brief  Resume the running program
void V5Dbg_ResumeProgram(v5dbg_server_state_t* pState);

/// @brief  Busy wait until the program is resumed, used to prevent execution in breakpoints0
void V5Dbg_WaitForSuspend(v5dbg_server_state_t *pState);