#pragma once
#include <memory>
#include "memory.h"
#include "v5dbg/debinfo.h"


/**
 * Handles setting the memory of a given stack variable using the type database
 * @param mem Variable to set the value of
 * @param pSet String to cast and copy into the variable
 * @return true if the operation was a success, false if otherwise
 */
bool V5Dbg_SetVariable(const std::shared_ptr<V5DbgMemoryObject> &mem, const std::string &pSet);