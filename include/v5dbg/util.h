#pragma once
#include <cstdarg>
#include <string>

/**
 * Operates similar to snprintf but produces an std::string buffer of a variable length
 * @param format Format parameters
 * @param ... Format values
 */
std::string V5Dbg_FormatPrint(const char* format, ...);

std::string V5Dbg_FormatPrint(const char* format, va_list list);

/**
 * Print data to the console in
 */
void info(const char* format, ...);

/**
 * Print data to the console in preinit
*/
void info_pre(const char* format, ...);