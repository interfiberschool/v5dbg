#pragma once
#include <string>
#include "v5dbg/debinfo.h"
#include "v5dbg/pretty.h"

/**
 * @brief  Stack frame memory information from $expose
 * Each function has its own stack frame memory object which is attached to the actual stack frame object when pushed
 */
struct v5dbg_stack_frame_memory_t
{
  /// @brief  Local memory exposed with just $expose
  std::vector<std::shared_ptr<V5DbgMemoryObject>> local;

  /// @brief  Global memory exposed with usually a call to $gexpose
  std::vector<std::shared_ptr<V5DbgMemoryObject>> global;
};

/// @brief  Stack frame information from $function
struct v5dbg_stack_frame_t
{
  /// @brief  Function name
  std::string funcName;

  /// @brief  Stack enter location
  v5dbg_code_point_t stackBegin{};

  /// @brief  Jump address of the function
  void* jmpAddress;

  /// @brief  Non-nullable stack memory object allocated by every function
  v5dbg_stack_frame_memory_t *pMemory;
};

/**
 * Stores memory information across function calls.
 * A V5DbgFunction is reallocated every time while its V5DbgStackMemory function is only allocated once per unique function
 */
class V5DbgStackMemory
{
public:
  V5DbgStackMemory() = default;

  /**
   * Expose a memory object to the debug server
   * @param mem Memory object to expose
   * @note 
   */
  void expose(const std::shared_ptr<V5DbgMemoryObject> &memObject);

  /**
   * Mark all allocations as deallocated while still storing their location information
   * @note Automatically called when a function scope ends
   */
  void deallocateAll();

  /// @brief  Return the underlying stack frame memory object
  [[nodiscard]] inline v5dbg_stack_frame_memory_t* getMemory()
  {
    return &m_memory;
  }

private:
  v5dbg_stack_frame_memory_t m_memory{};
};

/**
 * Created by a call to $function capturing stack information and reporting captured memory to the debugger
 */
class V5DbgFunction
{
public:
  V5DbgFunction(const std::string& name, const char* file, int line, void* pAddress, V5DbgStackMemory *memory);
  ~V5DbgFunction();

  /**
   * Expose a memory object to the debug server
   * @param mem Memory object to expose
   */
  void expose(const std::shared_ptr<V5DbgMemoryObject> &memObject);

private:
  V5DbgStackMemory* m_memory{};
};
