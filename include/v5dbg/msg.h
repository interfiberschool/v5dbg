#pragma once
#include "v5dbg/server.h"

/*
 * Server message handler functions
 */

/// @brief  Handle suspend program message
void V5Dbg_ServerSuspendHandle(v5dbg_server_state_t *pState, const v5dbg_message_t &msg);

/// @brief  Handle resume program message
void V5Dbg_ServerResumeHandle(v5dbg_server_state_t *pState, const v5dbg_message_t &msg);

/// @brief  
void V5Dbg_AllocateStringHandle(v5dbg_server_state_t *pState, const v5dbg_message_t &msg);

/// @brief  Handle returning the thread list to the client
void V5Dbg_ThreadListHandle(v5dbg_server_state_t *pState, const v5dbg_message_t &msg);

/// @brief  Handle returning the given virtual callstack to the client
void V5Dbg_VStackForHandle(v5dbg_server_state_t *pState, const v5dbg_message_t &msg);

/// @brief  Add a new server message handler
void V5Dbg_AddServerMessageHandler(v5dbg_server_state_t *pState, v5dbg_server_msg_callback_t callback);

/// @brief  Add all message handlers to the server state
void V5Dbg_PrimeServerMessageHandlers(v5dbg_server_state_t *pState);