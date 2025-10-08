#pragma once
#include <string>
#include "v5dbg/debinfo.h"

/// @brief  Stack frame information from $function
struct v5dbg_stack_frame_t
{
  /// @brief  Function name
  std::string funcName;

  /// @brief  Stack enter location
  v5dbg_code_point_t stackBegin{};

  /// @brief  Jump address of the function
  void* jmpAddress;
};

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

/**
 * Raw memory object which also manages the V5DbgPrettyPrinter
 */
template <auto T>
class V5DbgMemoryObject
{
public:
  /// Automatically infer the memory type based off T
  V5DbgMemoryObject() = default;

private:
  T* m_memory;
};

/**
 * Created by a call to $function capturing stack information and reporting captured memory to the debugger
 */
class V5DbgFunction
{
public:
  V5DbgFunction(const std::string& name, const char* file, int line, void* pAddress);

  /**
   * Expose a memory object to the debug server
   * @param mem Memory object to expose
   */
  void expose();

  ~V5DbgFunction();
};
