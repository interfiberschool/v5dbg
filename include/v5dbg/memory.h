#pragma once
#include <cstdint>
#include "v5dbg/debinfo.h"

/// @brief  Enum used to determine correct pretty printer function to use
enum v5dbg_memory_type_e
{
  /// @brief  Raw pointer, pretty printed as the memory address of the dest
  MEMORY_TYPE_PTR = 0,

  /// @brief  String which is represented by an array of characters, aka char*
  MEMORY_TYPE_CSTR,

  /// @brief  String which is represented by an std::string
  MEMORY_TYPE_STDSTR,

  /// @brief  Floating point number, if using a double use MEMORY_TYPE_DOUBLE
  MEMORY_TYPE_FLOAT,

  /// @brief  Double precision floating point number
  MEMORY_TYPE_DOUBLE,

  /// @brief  Base primitive integer type
  MEMORY_TYPE_BASE_INT,

  /// @brief  C++ std::vector<T> memory, the pretty printer only supports the base memory types when outputting
  MEMORY_TYPE_VECTOR,

  /// @brief  V5DbgMutex
  MEMORY_TYPE_MUTEX,

  /// @brief  pros::Motor
  MEMORY_TYPE_MOTOR,

  /// @brief  pros::MotorGroup
  MEMORY_TYPE_MOTORGROUP,

  /// @brief  Begin custom region
  MEMORY_TYPE_MAX
};

enum v5dbg_memory_state_e
{
  MEMORY_STATE_ALLOCATED = 0,
  MEMORY_STATE_DEALLOCATED = 1
};

/**
 * Raw memory object which also manages the V5DbgPrettyPrinter
 */
class V5DbgMemoryObject
{
public:
  /**
   * Create a memory object from variable information
   */
  explicit V5DbgMemoryObject(const v5dbg_variable_t &variable);

  static uint32_t getNextID()
  {
    static uint32_t cID = 0;
    cID++;

    return cID;
  }

  /// @brief  Set the memory object pointer
  void setPtr(void* ptr);

  /// @brief  Return this memory object's ID
  [[nodiscard]] inline uint32_t
  getID() const
  {
    return m_id;
  }

  [[nodiscard]] inline void*
  getPtr() const
  {
    return m_memory;
  }

  [[nodiscard]] inline v5dbg_variable_t
  getVariable() const
  {
    return m_variable;
  }

  /// @brief  Memory state
  v5dbg_memory_state_e memState = MEMORY_STATE_ALLOCATED;

private:
  uint32_t m_id;
  v5dbg_variable_t m_variable;

  void* m_memory;
  v5dbg_memory_type_e m_memoryType;
};
