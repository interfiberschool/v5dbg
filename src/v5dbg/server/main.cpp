#include "v5dbg/msg.h"
#include "v5dbg/server.h"
#include "v5dbg/util.h"

void
V5Dbg_ServerMain(v5dbg_server_state_t *pState)
{

  pState->ioTask = new pros::rtos::Task([pState]() { V5Dbg_ServerIOMain(pState); }, TASK_PRIORITY_MAX,
                                                TASK_STACK_DEPTH_DEFAULT, "v5dbg IO server");

  // Configure message handler list
  V5Dbg_PrimeServerMessageHandlers(pState);

  v5dbg_message_t open{};
  open.type = DEBUGGER_MESSAGE_OPEN;
  open.paramBuffer = "SERVEROPEN";

  V5Dbg_WriteToOut(V5Dbg_SerializeMessage(open));

  // Send an OPEN message to the debugger every once and awhile incase we miss the first one somehow
  pros::rtos::Task openPoll(
    []()
    {
      while (true)
      {
        v5dbg_message_t open{};
        open.type = DEBUGGER_MESSAGE_OPEN;
        open.paramBuffer = "SERVEROPEN";

        V5Dbg_WriteToOut(V5Dbg_SerializeMessage(open));

        pros::delay(2000);
      }
    });

  while (pState->canRun)
  {
    if (!V5Dbg_CanPump(pState))
    {
      pros::delay(10);
      continue;
    }

    try
    {
      const v5dbg_message_t message = V5Dbg_NextMessage(pState);

      bool f = false;

      for (auto& handler : pState->messageHandlers)
      {
        if (handler.messageType == message.type)
        {
          handler.handler(pState, message);
          f = true;

          break;
        }
      }

      if (!f)
      {
        info("Invalid message with type: %i", message.type);
      }
    }
    catch (std::exception& e)
    {
      info("MessageHandlerException: %s", e.what());
    }

    // Debugger delay of 10ms
    pros::delay(10);
  }
}
