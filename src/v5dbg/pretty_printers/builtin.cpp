// Pretty printers for builtin types like int, char, etc
#include <string>
#include "memory.h"
#include "v5dbg/util.h"
#include "v5dbg/pretty.h"

v5dbg_pretty_printed_t
V5Dbg_PrettyPrintInt(V5DbgMemoryObject *pMemory)
{
  return $pretty_print_result("int", pMemory->getVariable().name, V5Dbg_FormatPrint("%i", *((int*) pMemory->getPtr())));
}

v5dbg_pretty_printed_t
V5Dbg_PrettyPrintPtr(V5DbgMemoryObject *pMemory)
{
  return $pretty_print_result("void*", pMemory->getVariable().name, V5Dbg_FormatPrint("%p", pMemory->getPtr()));
}

v5dbg_pretty_printed_t
V5Dbg_PrettyPrintFloat(V5DbgMemoryObject *pMemory)
{
  return $pretty_print_result("float", pMemory->getVariable().name, V5Dbg_FormatPrint("%f", *((float*) pMemory->getPtr())));
}

v5dbg_pretty_printed_t
V5Dbg_PrettyPrintDouble(V5DbgMemoryObject *pMemory)
{
  return $pretty_print_result("double", pMemory->getVariable().name, V5Dbg_FormatPrint("%f", *((double*) pMemory->getPtr())));
}

v5dbg_pretty_printed_t
V5Dbg_PrettyPrintChar(V5DbgMemoryObject *pMemory)
{

  return $pretty_print_result("char", pMemory->getVariable().name, V5Dbg_FormatPrint("%c", *((char*) pMemory->getPtr())));
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