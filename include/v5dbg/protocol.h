#pragma once
#include <string>

/*
 * Example packet:
 * [PROTOCOL_VERSION]:[PACKET_TYPE]:[PACKET_DATA]
 */

/// Server protocol version
#define V5DBG_SERVER_VERSION 2

#define V5DBG_MSG_SEPERATOR ':'

enum v5dbg_message_type_e
{
  /// @brief  Connection opened
  DEBUGGER_MESSAGE_OPEN = 0,

  /// @brief  Request program suspension, assume it has occured when a DEBUG_MESSAGE_RSUSPEND is parsed
  DEBUGGER_MESSAGE_SUSPEND = 1,

  /// @brief  Connection closed
  DEBUGGER_MESSAGE_CLOSE = 2,

  /// @brief  Allocate a string, can be processed by the debugger however it likes
  DEBUGGER_MESSAGE_ALLOCATE_STRING = 3,

  /// @brief  Resume the program from a suspended state
  DEBUGGER_MESSAGE_RESUME = 4,

  /// @brief  Respond with DEBUGGER_MESSAGE_RTHREADS containing a comma seperated list of every thread being managed by
  /// v5dbg
  DEBUGGER_MESSAGE_THREADS = 5,

  /// @brief  Return message for DEBUGGER_MESSAGE_THREADS
  DEBUGGER_MESSAGE_RTHREADS = 6,

  /// @brief  Get the vstack for the given thread index
  DEBUGGER_MESSAGE_VSTACK_FOR = 7,

  /// @brief  Return message for DEBUGGER_MESSAGE_VSTACK_FOR, keep accepting messages until DEBUGGER_MESSAGE_VSTACK_END
  DEBUGGER_MESSAGE_RVSTACK = 8,

  /// @brief  Stop accepting DEBUGGER_MESSAGE_RVSTACK messages
  DEBUGGER_MESSAGE_VSTACK_END = 9,

  /// @brief  List memory for the given stack frame with thread ID
  DEBUGGER_MESSAGE_LMEM_FOR = 10,

  /// @brief  Returned message for DEBUGGER_MESSAGE_LMEM_FOR, keep accepting messages until DEBUGGER_MESSAGE_LMEM_END
  DEBUGGER_MESSAGE_RLMEM = 11,

  /// @brief  Stop accepting DEBUGGER_MESSAGE_RLMEM messages
  DEBUGGER_MESSAGE_LMEM_END = 12,

  /// @brief  Sent to the debugger every time a breakpoint is activated and the program is suspended
  DEBUGGER_MESSAGE_BREAK_INVOKED = 13,

  /// @brief  Max debugger message ID
  DEBUGGER_MESSAGE_MAX = 14
};

struct v5dbg_message_t
{
  /// @brief  Message type
  v5dbg_message_type_e type;

  /// @brief  Message parameter buffer
  std::string paramBuffer;
};

/// @brief  Serialize a message from a v5dbg_message_t object
std::string V5Dbg_SerializeMessage(v5dbg_message_t message);

/// @brief  Deserialize a message from a std::string
/// @param msg Input message data string
/// @return Deserialized message
v5dbg_message_t V5Dbg_DeserializeMessage(const std::string& msg);
