// Pretty printers for builtin types like int, char, etc
#include <string>
#include "memory.h"
#include "v5dbg/util.h"
#include "v5dbg/pretty.h"

std::string
V5Dbg_PrettyPrintInt(V5DbgMemoryObject *pMemory)
{
  return V5Dbg_FormatPrint("int %s = %i", pMemory->getVariable().name.c_str(), *((int*) pMemory->getPtr()));
}

std::string
V5Dbg_PrettyPrintPtr(V5DbgMemoryObject *pMemory)
{
  return V5Dbg_FormatPrint("void* %s = %p", pMemory->getVariable().name.c_str(), pMemory->getPtr());
}

std::string
V5Dbg_PrettyPrintFloat(V5DbgMemoryObject *pMemory)
{
  return V5Dbg_FormatPrint("float %s = %f", pMemory->getVariable().name.c_str(), *(float* ) pMemory->getPtr());
}

std::string
V5Dbg_PrettyPrintDouble(V5DbgMemoryObject *pMemory)
{
  return V5Dbg_FormatPrint("double %s = %f", pMemory->getVariable().name.c_str(), *(double* ) pMemory->getPtr());
}

std::string
V5Dbg_PrettyPrintChar(V5DbgMemoryObject *pMemory)
{
  return V5Dbg_FormatPrint("char %s = '%c'", pMemory->getVariable().name.c_str(), *(char* ) pMemory->getPtr());
}

$pretty_printer(V5Dbg_PrettyPrintInt, MEMORY_TYPE_BASE_INT);
$link_type_db(int, MEMORY_TYPE_BASE_INT);

$pretty_printer(V5Dbg_PrettyPrintFloat, MEMORY_TYPE_FLOAT);
$link_type_db(float, MEMORY_TYPE_FLOAT);

$pretty_printer(V5Dbg_PrettyPrintDouble, MEMORY_TYPE_DOUBLE);
$link_type_db(double, MEMORY_TYPE_DOUBLE);

$pretty_printer(V5Dbg_PrettyPrintPtr, MEMORY_TYPE_PTR);
$link_type_db(void*, MEMORY_TYPE_PTR);

$pretty_printer(V5Dbg_PrettyPrintChar, MEMORY_TYPE_CHAR);
$link_type_db(char, MEMORY_TYPE_CHAR);