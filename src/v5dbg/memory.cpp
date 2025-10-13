#include "v5dbg/pretty.h"

V5DbgMemoryObject::V5DbgMemoryObject()
{
    m_id = getNextID();
}

void
V5DbgMemoryObject::setPtr(void* ptr)
{
  m_memory = ptr;
}