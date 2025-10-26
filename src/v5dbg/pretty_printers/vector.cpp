// Pretty printers for std::vectors of supported data types

#include <string>
#include "memory.h"
#include "v5dbg/util.h"
#include "v5dbg/pretty.h"

/// @brief  Ugly macro used to generate pretty printers for specific std::vector templates
#define $pretty_printer_vec(typeReadable, typeCpp, fmt) \
  v5dbg_pretty_printed_t \
  V5Dbg_PrettyPrintVector##typeReadable(V5DbgMemoryObject *pMem) \
  { \
  std::vector<typeCpp> v = *(std::vector<typeCpp>*) pMem->getPtr(); \
  v5dbg_pretty_printed_t r{}; \
  r.typeName = "std::vector<" + std::string(#typeCpp) + ">"; \
  r.varName = pMem->getVariable().name; \
  r.printBuffer = "{"; \
  for (int i = 0; i < v.size(); i++) \
  { \
    r.printBuffer += V5Dbg_FormatPrint(fmt, v[i]); \
    if (i + 1 < v.size()) r.printBuffer += ","; \
  } \
  r.printBuffer += "}"; \
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