#include "debinfo.h"
#include "v5dbg/pretty.h"

V5DbgMemoryObject::V5DbgMemoryObject(const v5dbg_variable_t &var)
{
    m_variable = var;
    m_id = getNextID();
}

void
V5DbgMemoryObject::setPtr(const void* ptr)
{
  m_memory = ptr;
}