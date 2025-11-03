#pragma once

/*
 * Internal bindings to the VEX SDK API
 * Instead of binding to the jumptable we can import functions from libv5rts which is built into libpros
 * using extern "C"
 */

/**
 * Request the program to exit and return to the user programs screen
 * @note Functions the exact same as 'void exit(int code)'
 */
extern "C" void vexSystemExitRequest( void );