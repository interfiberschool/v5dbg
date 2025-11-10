#include "v5dbg/memory.h"
#include <cstring>
#include "v5dbg/debinfo.h"
#include "v5dbg/util.h"

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

  // Copy constant data to override this memory object
  if (m_recopy != nullptr)
  {
      if (!setBuffer(m_recopy))
      {
          info("SetBuffer failed to recopy!");
      }
  }
}

V5DbgDeallocator::~V5DbgDeallocator()
{
  m_obj->memState = MEMORY_STATE_DEALLOCATED;
  m_obj->setPtr(nullptr);
}

bool
V5DbgMemoryObject::setBuffer(void* pBuffer)
{
  if (memState == MEMORY_STATE_DEALLOCATED || m_memory == nullptr)
  {
    info("Cannot setBuffer on unallocated object!");
    return false;
  }

  // C++ blackmagic fuckery to convert a immutable pointer to a mutable one
  memcpy(const_cast<void*>(m_memory), pBuffer, m_memSize);

  return true;
}

void
V5DbgMemoryObject::setRecopyBuffer(void* pBuffer)
{
    m_recopy = pBuffer;
}
