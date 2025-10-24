---
description: The only true VEX debugger™
---

# V5 Debugger

The only true VEX debugger™

!!! example "V5dbg is still experimental"

    v5dbg is still under **HEAVY** development and the documentation may not reflect the current state of the library and program.

    [:octicons-bug-24: Bug Tracker](https://github.com/Interfiber/v5dbg/issues)

    [:octicons-tag-24: Releases Page](https://github.com/Interfiber/v5dbg/releases)

## What can v5dbg do?

<div class="grid cards" markdown>

- :fontawesome-solid-circle: Set software breakpoints

    ---
    - Set breakpoints on function entrance/exit, memory allocations, and in manual locations.
    - Conditional breakpoints `$cbreak`

    [:octicons-arrow-right-24: C++ Documentation](cpp/macros/debug/function.md)

    [:octicons-arrow-right-24: Debugger Documentation](debugger/commands.md#Breakpoints)

- :fontawesome-solid-microchip: Inspect active threads


    ---
    - View active locks and which threads hold them
    - View the current callstack for a thread at any time
    - Easily switch the debuggers active context to another thread

    [:octicons-arrow-right-24: C++ Documentation](cpp/macros/debug/ntask.md)

    [:octicons-arrow-right-24: Debugger Documentation](debugger/commands.md#Threads)

- :fontawesome-solid-memory: Inspect, set, and manage memory

    ---
    - Automatically pretty print variables based on compile-time type information
    - Set memory value to a constant, variable constant, or temporary value

    [:octicons-arrow-right-24: C++ Documentation](cpp/macros/memory)

    [:octicons-arrow-right-24: Debugger Documentation](debugger/commands.md#Memory)

- :fontawesome-brands-usb: Inspect device states

    ---
    - Motor information
    - Battery power
    - Connected remote information
    - Radio I/O

    [:octicons-arrow-right-24: C++ Documentation](macros/device)

    [:octicons-arrow-right-24: Debugger Documentation](debugger/commands.md#Devices)

</div>

[Ready to get started?](install/server.md){ .md-button .md-button--primary }