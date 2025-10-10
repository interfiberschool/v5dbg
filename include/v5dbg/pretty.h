#pragma once
#include <string>

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
class V5DbgMemoryObject
{
public:
  /// Automatically infer the memory type based off T
  V5DbgMemoryObject() = default;

private:
  void* m_memory;
  v5dbg_memory_type_e m_memoryType;
};

/**
 * Handles pretty-printing raw memory objects based on type
 * @note We just cast memory addresses to whatever the fuck we want here
 */
class V5DbgPrettyPrinter {
public:
  explicit V5DbgPrettyPrinter(V5DbgMemoryObject *pMemory);

  /// @brief  Generate the printable string
  /// @return Pretty printable string
  [[nodiscard]] virtual std::string getPrintable() = 0;

  /**
   * Send the pretty printed string to stdout
   */
  void print();

protected:
  V5DbgMemoryObject *m_target;
};

#define $pretty_printer(className) \
  class className : public V5DbgPrettyPrinter \

/**
 * Memory address (aka pointer) pretty printer
 */
$pretty_printer(V5DbgPtrPrettyPrinter) {
public:
  explicit V5DbgPtrPrettyPrinter(V5DbgMemoryObject* pMemory) : V5DbgPrettyPrinter(pMemory) {};

  [[nodiscard]] std::string getPrintable() override;
};