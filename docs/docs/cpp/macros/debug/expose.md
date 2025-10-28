---
description: Documentation for the $expose macro which is used to expose memory to thd debugger
icon: octicons/arrow-switch-24
---

# `$expose`

!!! abstract "Version information"
    Introduced in version **v0.1** :octicons-tag-24:

    This macro is considered **stable** :octicons-check-24:

## About

The `$expose` macro allows v5dbg to **expose variables** to the debugger. The exposed variables can be **viewed and modified** later using debugger commands such as [`print`](../../../debugger/cmds/print.md)

??? question "Why do I need to use this macro?"
    V5dbg **cannot see** where local variables are **in memory**, see [the engineering page](../../../debug_server/exposed_memory.md) for more information.

## Notes

!!! danger "Required environment"
    - This macro **requires** the debug server to have been initialized before being called.
    - This macro **requires** the current thread to be supervised with [$ntask](./ntask.md) or `V5Dbg_Init`
    - This macro **requires** the current function to be [debuggable](../debug/function.md4)

## Examples

=== "Single scope"

    ```c++ hl_lines="11 12 17" linenums="1"
    #include "v5dbg/debug.h"

    void
    opcontrol()
    {
        $ntask
        $function

        int i = 0; // Incrementor

        float randomData = 0;
        $expose(randomData); // (1)

        while (true)
        {
            // Add some junk to our variable
            randomData += (i * 5) / 3.3333;

            pros::delay(300);

            i++;
        }
    }
    ```

    1. Here we allocate a new `float` variable on the stack and **expose** it with `$expose`. We only need to do this when a variable **is allocated** and any changes made to the variable afterwards will be **automatically reflected** in the debugger.

=== "Multiple scopes"

    ```c++ hl_lines="6" linenums="1"
    #include "v5dbg/debug.h"

    void
    printAndSleep(const std::string &p)
    {
        $function // (2)
        pros::lcd::print(1, "%s", p.c_str()); // Print our data to the screen

        pros::delay(300); // Wait 300ms
    }

    void
    opcontrol()
    {
        $ntask // (1)
        $function

        while (true)
        {
            printAndSleep("Hello World");
        }
    }
    ```


    1. For more information on `$ntask` look [here](./ntask.md)
    2. Now our `printAndSleep` function will be the second item in the callstack, it should now look like this:
        - `void printAndSleep(const std::string &p)`
        - `void opcontrol()`