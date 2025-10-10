#include "v5dbg/pretty.h"

V5DbgPrettyPrinter::V5DbgPrettyPrinter(V5DbgMemoryObject *pMemory)
{
  m_target = pMemory;
}

void V5DbgPrettyPrinter::print()
{
  printf("%s\n", getPrintable().c_str());
}