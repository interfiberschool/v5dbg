#include "v5dbg/memory.h"
#include "v5dbg/util.h"
#include "v5dbg/pretty.h"

std::string
V5Dbg_PrettyPrintString(V5DbgMemoryObject *pMem)
{
  return V5Dbg_FormatPrint("std::string %s = \"%s\"", pMem->getVariable().name.c_str(), (*(std::string*) pMem->getPtr()).c_str());
}

$pretty_printer(V5Dbg_PrettyPrintString, MEMORY_TYPE_STDSTR);
$link_type_db(std::string, MEMORY_TYPE_STDSTR);