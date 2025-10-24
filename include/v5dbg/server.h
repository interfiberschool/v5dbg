#pragma once
#include <queue>
#include <vector>
#include "pros/rtos.hpp"
#include "v5dbg/protocol.h"

struct v5dbg_server_state_t;
struct v5dbg_thread_t;
typedef void (*V5Dbg_ServerMsgCallback)(v5dbg_server_state_t *pState, const v5dbg_message_t &msg);

struct v5dbg_server_msg_callback_t
{
  /// @brief  Message type to handle
  v5dbg_message_type_e messageType;

  /// @brief  Non-null pointer to the server message handler
  V5Dbg_ServerMsgCallback handler;
};

/// @brief  Server control state
struct v5dbg_server_state_t
{
  /// @brief  Used to lock the list of managed threads
  pros::rtos::Mutex* threadListLock;

  /// @brief List of managed threads which have called V5Dbg_Init()
  std::vector<v5dbg_thread_t> threads;

  /// @brief  Lock the message queue during event pumping
  pros::rtos::Mutex* messageQueueLock;

  /// @brief  Message queue
  std::queue<v5dbg_message_t> messageQueue;

  /// @brief  Server task object
  pros::rtos::Task* serverTask;

  /// @brief  Server IO task
  pros::rtos::Task* ioTask;

  /// @brief  List of registered message handlers
  std::vector<v5dbg_server_msg_callback_t> messageHandlers;

  /// @brief  Turned to false when the server needs to be suspended
  bool canRun = true;
};

[[maybe_unused]] static v5dbg_server_state_t* CURRENT_SERVER = nullptr;

/**
 * Should be called as early as possible to start the debugger server
 * @brief Start the local debugger server
 * @param pState Allocated state object to use
 */
void V5Dbg_StartServer(v5dbg_server_state_t* pState);

/**
 * Write a text buffer to the serial output stream
 * @param msg Text buffer to write
 */
void V5Dbg_WriteToOut(const std::string &msg);

/// @brief  Should be called as the first line of code in a new task, allows the debugger to manage this task
v5dbg_thread_t* V5Dbg_Init();

/// @brief  Can be called to add another task object to the debugger
v5dbg_thread_t* V5Dbg_RemoteInit(pros::rtos::Task other);

/// @brief  Stop supervising the given thread
void V5Dbg_Leave(v5dbg_thread_t* pThread);

/// @brief  Allocate a new server state object
v5dbg_server_state_t V5Dbg_AllocateServerState();

/// @brief  Allocate a new server thread object
v5dbg_thread_t V5Dbg_AllocateServerThread();

/// @brief  Return the v5dbg_thread_t* for the current task
v5dbg_thread_t* V5Dbg_ThreadForTask(v5dbg_server_state_t *pState);

/// @brief  Uses CURRENT_SERVER when calling V5Dbg_ThreadForTask
v5dbg_thread_t* V5Dbg_ThreadForTask();

/// @brief  Uses CURRENT_SERVER when calling V5Dbg_ThreadForTask
v5dbg_thread_t* V5Dbg_ThreadWithID(v5dbg_server_state_t* pState, int id);

/// @brief  Return the v5dbg_thread_t for the given task
v5dbg_thread_t* V5Dbg_ThreadWithID(int id);

/// @brief  Internal server main function, should never be called manually
void V5Dbg_ServerMain();

/// @brief  Debug server IO thread
void V5Dbg_ServerIOMain(v5dbg_server_state_t *pState);

/// @brief  Can we pump another message from the debugger message queue
bool V5Dbg_CanPump(const v5dbg_server_state_t *pState);

/// @brief  Return the next message in the queue
v5dbg_message_t V5Dbg_NextMessage(v5dbg_server_state_t *pState);

/// @brief  Push a message into the outbound message queue
void V5Dbg_PushMessage(v5dbg_server_state_t *pState, const v5dbg_message_t& message);
