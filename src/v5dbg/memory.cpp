#include "memory.h"
#include <cstring>
#include "debinfo.h"
#include "util.h"
#include "v5dbg/pretty.h"

V5DbgMemoryObject::V5DbgMemoryObject(const v5dbg_variable_t& var, size_t memSize)
{
  m_variable = var;
  m_memSize = memSize;
  m_id = getNextID();
}

void
V5DbgMemoryObject::setPtr(const void* ptr)
{
  m_memory = ptr;
}

V5DbgDeallocator::~V5DbgDeallocator()
{
  m_obj->memState = MEMORY_STATE_DEALLOCATED;
  m_obj->setPtr(nullptr);
}

void
V5DbgMemoryObject::setBuffer(void* pBuffer)
{
  if (m_memory == nullptr)
  {
    info("Cannot setBuffer on unallocated object!");
  }

  // C++ blackmagic fuckery to convert a immutable pointer to a mutable one
  memcpy(const_cast<void*>(m_memory), pBuffer, m_memSize);
}