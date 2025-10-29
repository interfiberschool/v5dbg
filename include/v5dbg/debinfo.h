#pragma once
#include <string>
#include <vector>
#include "pros/rtos.hpp"

/// @brief  Describes a specific location in the programs source code
struct v5dbg_code_point_t
{
  /// @brief  Path to the source code file relative to the project directory
  std::string filePath;

  /// @brief  Line number which the code point is on
  int lineNumber;
};

/// @brief  Describes a variable located in the program
struct v5dbg_variable_t
{
  /// @brief  Variable name
  std::string name;

  /// @brief  Variable type name which can be optionally used by the pretty printer
  std::string typeName;

  /// @brief  Allocation point
  v5dbg_code_point_t allocationPoint;
};

struct v5dbg_stack_frame_t;

/// @brief Thread with a stack trace
struct v5dbg_thread_t
{
  /// @brief  Name of the thread, by default this is the task name
  std::string name;

  /// @brief  Underlying task object for this thread
  pros::rtos::Task task = pros::rtos::Task::current();

  /// @brief  Locked when modifiying any debugger stored data for this thread
  pros::rtos::Mutex* threadLock;

  /// @brief  Allocate thread stack
  std::vector<v5dbg_stack_frame_t> stack;
};