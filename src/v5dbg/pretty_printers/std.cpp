#include "v5dbg/memory.h"
#include "v5dbg/util.h"
#include "v5dbg/pretty.h"

v5dbg_pretty_printed_t
V5Dbg_PrettyPrintString(V5DbgMemoryObject *pMem)
{
  return $pretty_print_result("std::string", pMem->getVariable().name, V5Dbg_FormatPrint("\"%s\"", (*(std::string*) pMem->getPtr()).c_str()));
}

$pretty_printer(V5Dbg_PrettyPrintString, MEMORY_TYPE_STDSTR);
$link_type_db(std::string, MEMORY_TYPE_STDSTR);