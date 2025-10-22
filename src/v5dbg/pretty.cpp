#include "v5dbg/pretty.h"
#include <typeinfo>
#include "memory.h"
#include "util.h"

v5dbg_memory_type_e
V5Dbg_MemoryTypeFromType(const std::type_info& typeInfo)
{
  for (auto& k : V5Dbg_GetPrettyPrinterState()->typeDb)
  {
    if (k.first == typeInfo.hash_code())
    {
      return k.second;
    }
  }

  return MEMORY_TYPE_PTR;
}

V5Dbg_PrettyPrintMemoryObj
V5Dbg_PrettyPrinterFromType(v5dbg_memory_type_e memType)
{
  for (auto& pp : V5Dbg_GetPrettyPrinterState()->printers)
  {
    if (pp.first == memType)
      return pp.second;
  }

  return nullptr;
}

void
V5Dbg_RegisterPrettyPrinter(v5dbg_memory_type_e memType, V5Dbg_PrettyPrintMemoryObj func)
{
  V5Dbg_GetPrettyPrinterState()->printers.insert({ memType, func });
}

std::string
V5Dbg_PrettyPrint(V5DbgMemoryObject *pMem)
{
  V5Dbg_PrettyPrintMemoryObj printer = V5Dbg_PrettyPrinterFromType(pMem->getMemoryType());
  if (printer == nullptr)
    return V5Dbg_FormatPrint("%p (default)", pMem->getPtr());

  return printer(pMem);
}