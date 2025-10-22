#include "v5dbg/util.h"
#include <cstdarg>

std::string
V5Dbg_FormatPrint(const char *format, va_list args)
{
// Determine correct buffer size
  int size = vsnprintf(nullptr, 0, format, args);
  if (size == 0) return "";

  size += 1;

  char* buffer = (char* ) malloc(size * sizeof(char));

  if (vsnprintf(buffer, size, format, args) <= 0)
  {
    printf("V5Dbg_FormatPrint(...): Failed to encode output string with size of: %i", size);
  }

  // Convert heap allocated buffer into an std::string
  std::string result(buffer);
  free(buffer);

  return result;
}

std::string
V5Dbg_FormatPrint(const char* format, ...)
{
  va_list args;

  va_start(args, format);

  std::string result = V5Dbg_FormatPrint(format, args);

  va_end(args);

  return result;
}

void info(const char* format, ...)
{
  va_list args;

  va_start(args, format);

  printf("(v5dbg) %s\n", V5Dbg_FormatPrint(format, args).c_str());

  va_end(args);
}


void info_pre(const char* format, ...)
{
  va_list args;

  va_start(args, format);

  printf("(v5dbg-sys-init) %s\n", V5Dbg_FormatPrint(format, args).c_str());

  va_end(args);
}