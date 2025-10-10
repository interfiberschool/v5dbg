#include "v5dbg/pretty.h"
#include "v5dbg/util.h"

// Pointer-based pretty printers

std::string
V5DbgPtrPrettyPrinter::getPrintable()
{
  return V5Dbg_FormatPrint("%p", m_target);
}