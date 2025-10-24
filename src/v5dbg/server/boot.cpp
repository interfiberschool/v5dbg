/*
 * Displays v5dbg version info on program init (before pros)
*/

#include <cerrno>
#include "v5dbg/protocol.h"
#include "v5dbg/util.h"

class V5DbgBootManager
{
public:
  V5DbgBootManager()
  {
    FILE* sout = fopen("sout", "w");
    int err = errno;

    printf("\n\n"); // Spacing

    info_pre("V5 Debugger active!");

    info_pre("Protocol version: %i\tMessage seperator: '%c'", V5DBG_SERVER_VERSION, V5DBG_MSG_SEPERATOR);
    info_pre("----");
    info_pre("Github: https://github.com/Interfiber/v5dbg.git");
    info_pre("Website: https://v5dbg.beachmont.xyz");
    info_pre("Copyright (C) v5dbg contributors 2025");
    info_pre("This program has been placed under the MIT license");
    info_pre("Serial port FD: %p (%i)", sout, err);
  }

  ~V5DbgBootManager()
  {
    // Never called since program exiting leads to termination and immediate memory cleanup without calling destructors
    info_pre("Managed program has exited");
  }
};

// Static will make sure this is allocated before any user control functions are called
static V5DbgBootManager _v5dbg_boot_mgr;