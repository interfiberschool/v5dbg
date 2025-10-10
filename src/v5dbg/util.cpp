#include "v5dbg/util.h"
#include <cstdarg>

std::string
V5Dbg_FormatPrint(const char* format, ...)
{
  va_list args;

  va_start(args, format);

  // Determine correct buffer size
  int size = vsnprintf(nullptr, 0, format, args);
  if (size == 0) return "";

  char* buffer = (char* ) malloc(size * sizeof(char));

  if (vsnprintf(buffer, size, format, args) <= 0)
  {
    printf("V5Dbg_FormatPrint(...): Failed to encode output string with size of: %i\n", size);
  }

  va_end(args);

  // Convert heap allocated buffer into an std::string
  std::string result(buffer);
  free(buffer);

  return result;
}