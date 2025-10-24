# Integration

## Step 1. Allocate the server state object

v5dbg relies on a core server state object to contain the debuggers state. Find a place in your program like `main.cpp` where you can place the global server state object like below:

```c++
// .. snip ..
#include "v5dbg/server.h"

v5dbg_server_state_t serverState{};
```

Now we can initialize it with `V5Dbg_AllocateServerState` inside our `initialize` function like so

```c++
void
initialize()
{
    // Allocate server state heap resources
    serverState = V5Dbg_AllocateServerState();
}
```

## Step 2. Start the debug server

In order to start integrating v5dbg into our bot code we need to actually start the debug server. Still in our `initialize` function we can add a call to `V5Dbg_StartServer` which takes in a pointer to the `v5dbg_server_state_t` object we allocated in the previous step. Our file should now look similar to whats below

```c++
#include "v5dbg/server.h"

v5dbg_server_state_t serverState{};

void
initialize()
{
    // Allocate server state heap resources
    serverState = V5Dbg_AllocateServerState();

    // Start the debug server
    V5Dbg_StartServer(&serverState);
}
```

## Step 3. Inform the debugger of new tasks

Right now the debug server is waiting for messages and API calls. We need to tell the debug server of any new tasks that we create, including ones automatically created by the PROS system daemon, such as `opcontrol`. Lets just to the first line of code in our `opcontrol` function.

Here lets tell the debugger about the new task using `V5Dbg_Init`

```c++
void
opcontrol()
{
    // Will automatically tell the debugger to supervise execution of the current task
    V5Dbg_Init();

    // If we want to be more verbose we can use the following which is what V5Dbg_Init does behind the scenes.
    V5Dbg_RemoteInit(pros::rtos::Task::current_task());

    while (true)
    {
        // ... opcontrol code ...
    }

    // Our task is about to be deleted so inform the debugger to stop supervising it
    V5Dbg_Leave();
}
```

V5dbg also offers a macro named `$ntask` which will automatically supervise and shutdown resources as needed.

```c++
#include "v5dbg/debug.h" // Needed for all debug macros like $ntask

void opcontrol()
{
    $ntask

    while (true)
    {
        // ... opcontrol code ...
    }
}

```

## Step 4. Start tracking function calls

Now we can use normal debugging macros! At the start of every function we can place a call to `$function` which will allow the debugger to generate stack traces in realtime when pausing our program. You should also make sure to call `$function` after informing the debugger of the `opcontrol` task so it shows up in stack traces!

```c++
void 
printData(const std::string &msg)
{
    $function

    printf("%s\n", msg.c_str());

    pros::delay(1000); // So we can see `printData` in the callstack!
}
```

For more information on debugger macros see the [Macros](../cpp/macros/debug/function.md) section, or view the [Debugger Client](../install/debugger.md) documentation.
