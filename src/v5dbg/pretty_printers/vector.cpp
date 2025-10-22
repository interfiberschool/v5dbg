// Pretty printers for std::vectors of supported data types

#include <string>
#include "memory.h"
#include "v5dbg/util.h"
#include "v5dbg/pretty.h"

#define $pretty_printer_vec(typeReadable, typeCpp, fmt) \
  std::string \
  V5Dbg_PrettyPrintVector##typeReadable(V5DbgMemoryObject *pMem) \
  { \
  std::vector<typeCpp> v = *(std::vector<typeCpp>*) pMem->getPtr(); \
  std::string r = V5Dbg_FormatPrint("std::vector<%s> %s = {", #typeCpp, pMem->getVariable().name.c_str()); \
  for (int i = 0; i < v.size(); i++) \
  { \
    r += V5Dbg_FormatPrint(fmt, v[i]); \
    if (i + 1 < v.size()) r += ","; \
  } \
  r += "}"; \
  return r; \
} \

$pretty_printer_vec(Int, int, "%i")
$pretty_printer_vec(Float, float, "%f")
$pretty_printer_vec(Double, double, "%f")

$pretty_printer(V5Dbg_PrettyPrintVectorInt, MEMORY_TYPE_IVEC);
$link_type_db(std::vector<int>, MEMORY_TYPE_IVEC);

$pretty_printer(V5Dbg_PrettyPrintVectorFloat, MEMORY_TYPE_FVEC);
$link_type_db(std::vector<float>, MEMORY_TYPE_FVEC);

$pretty_printer(V5Dbg_PrettyPrintVectorDouble, MEMORY_TYPE_DVEC);
$link_type_db(std::vector<double>, MEMORY_TYPE_DVEC);