# `$ntask`

!!! abstract "Version information"
    Introduced in version **v0.1** :octicons-tag-24:

    This macro is considered **unavailable** :octicons-x-circle-fill-24:

## About

The `$ntask` macro informs the debug server of a newly spawned thread/task. It should be the **first line of code** ever executed during a tasks runtime, otherwise other debug macros may not work.

!!! warning "Common pitfall"
    When `$ntask` falls out of scope it will automatically **prevent the debugger from supervising the task**, make sure that the scope its called in lives until the task is ready to end.

## Notes

!!! danger "Required environment"
    - This macro **requires** the debug server to have been initialized before being called.

## Example

```c++ hl_lines="6" linenums="1"
#include "v5dbg/debug.h"

void
opcontrol()
{
    $ntask // (1)!
    $function // (2)!

    while (true)
    {
        // Print "Hello World" to the screen via pros::lcd
        pros::lcd::print(1, "Hello World");

        pros::delay(300);
    }
}
```

1. Our thread is now **supervised** and we can begin to use other debug macros.
2. For more information on `$function` look [here](./function.md)