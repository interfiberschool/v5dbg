#pragma once
#include <string>

/**
 * Operates similar to snprintf but produces an std::string buffer of a variable length
 * @param format Format parameters
 * @param ... Format values
 */
std::string V5Dbg_FormatPrint(const char* format, ...);