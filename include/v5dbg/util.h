#pragma once
#include <cstdarg>
#include <string>
#include <vector>

/**
 * Operates similar to snprintf but produces an std::string buffer of a variable length
 * @param format Format parameters
 * @param ... Format values
 */
std::string V5Dbg_FormatPrint(const char* format, ...);

std::string V5Dbg_FormatPrint(const char* format, va_list list);

/**
 * Demangle the given symbol using the internal GNU G++ ABI functions
 * @param symbol Symbol to demangle
 * @return Demangled symbol
 */
std::string V5Dbg_Demangle(const char* symbol);

/**
 * Print data to the console in
 */
void info(const char* format, ...);

/**
 * Print data to the console in preinit
 */
void info_pre(const char* format, ...);

#define CONCAT_(prefix, suffix) prefix##suffix
#define CONCAT(prefix, suffix) CONCAT_(prefix, suffix)

inline std::vector<std::string>
V5Dbg_SplitString(const std::string& s, const std::string& delimiter)
{
  std::vector<std::string> tokens;
  size_t pos_start = 0, pos_end;
  size_t delim_len = delimiter.length();
  std::string token;

  while ((pos_end = s.find(delimiter, pos_start)) != std::string::npos)
  {
    token = s.substr(pos_start, pos_end - pos_start);
    pos_start = pos_end + delim_len;
    tokens.push_back(token);
  }
  tokens.push_back(s.substr(pos_start)); // Add the last token
  return tokens;
}
