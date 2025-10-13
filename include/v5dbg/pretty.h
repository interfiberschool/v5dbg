#pragma once
#include <string>
#include "v5dbg/memory.h"

/**
 * Handles pretty-printing raw memory objects based on type
 * @note We just cast memory addresses to whatever the fuck we want here
 */
class V5DbgPrettyPrinter
{
public:
  explicit V5DbgPrettyPrinter(V5DbgMemoryObject* pMemory);

  /// @brief  Generate the printable string
  /// @return Pretty printable string
  [[nodiscard]] virtual std::string getPrintable() = 0;

  /**
   * Send the pretty printed string to stdout
   */
  void print();

protected:
  V5DbgMemoryObject* m_target;
};

#define $pretty_printer(className) class className : public V5DbgPrettyPrinter

/**
 * Memory address (aka pointer) pretty printer
 */
$pretty_printer(V5DbgPtrPrettyPrinter)
{
public:
  explicit V5DbgPtrPrettyPrinter(V5DbgMemoryObject * pMemory) : V5DbgPrettyPrinter(pMemory){};

  [[nodiscard]] std::string getPrintable() override;
};
