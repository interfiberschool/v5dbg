#pragma once

/*
 * V5dbg debug server configuration
 * Any changes made here require a recompile to take effect
*/

/**
 * @brief Uncomment to disable all debugger functionality
 * All debugger functions are replaced by stubbed versions located in src/stubs.cpp which is only compiled when this macro is defined
*/
// #define V5DBG_DEBUGGER_DISABLE 