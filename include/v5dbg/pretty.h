#pragma once
#include <typeinfo>
#include <unordered_map>
#include "v5dbg/memory.h"

/// @brief  Function pointer to pretty printer impl
typedef void (*V5Dbg_PrettyPrintMemoryObj)(V5DbgMemoryObject *pMemory);

struct v5dbg_pretty_printer_state_t
{
  /// @brief  Collection of pretty printers for each memory object type
  std::unordered_map<v5dbg_memory_type_e, V5Dbg_PrettyPrintMemoryObj> printers;

  /// @brief  Automatic type detection database where the key is the hash_code provided by std::type_info
  std::unordered_map<std::size_t, v5dbg_memory_type_e> typeDb;
};

/// @brief  Return the global pretty printer state object
inline v5dbg_pretty_printer_state_t* V5Dbg_GetPrettyPrinterState()
{
  static v5dbg_pretty_printer_state_t state{};

  return &state;
}


/**
 * @brief  Detect the memory object type from the compilers provided std::type_info, def
 * @return Correct type, if no type is found we default to a raw pointer
*/
v5dbg_memory_type_e V5Dbg_MemoryTypeFromType(const std::type_info &typeInfo);

/**
 * @brief  Find the correct pretty printer to use for the given memory type
 * @return Correct pretty printer or nullptr if none was found
 */
V5Dbg_PrettyPrintMemoryObj V5Dbg_PrettyPrinterFromType(v5dbg_pretty_printer_state_t *pState, v5dbg_memory_type_e memType);

/// @brief  Register a pretty printer with a C++ type 
#define $pretty_printer(func, type)