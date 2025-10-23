# V5 Debugger

The only true VEX debugger™

!!! example "V5dbg is still **EXPERIMENTAL**"

    v5dbg is still under **HEAVY** development and the documentation may not reflect the current state of the library and program.

    [:octicons-bug-24: Bug Tracker](https://github.com/Interfiber/v5dbg/issues)

    [:octicons-tag-24: Releases Page](https://github.com/Interfiber/v5dbg/releases)

[Ready to get started?](install.md){ .md-button .md-button--primary }

## What can v5dbg do?

<div class="grid cards" markdown>

- :fontawesome-solid-circle: Set software breakpoints

    ---
    - Set breakpoints on function entrance/exit, memory allocations, and in manual locations.
    - Conditional breakpoints `$cbreak`

    [:octicons-arrow-right-24: C++ Documentation](macros.md#break)

    [:octicons-arrow-right-24: Debugger Documentation](commands.md)

- :fontawesome-solid-microchip: Inspect active threads


    ---
    - View active locks and which threads hold them
    - View the current callstack for a thread at any time
    - Easily switch the debuggers active context to another thread

    [:octicons-arrow-right-24: C++ Documentation](macros.md#ntask)

    [:octicons-arrow-right-24: Debugger Documentation](commands.md)

- :fontawesome-solid-memory: Inspect, set, and manage memory

    ---
    - Automatically pretty print variables based on compile-time type information
    - Set memory value to a constant, variable constant, or temporary value

    [:octicons-arrow-right-24: C++ Documentation](macros.md#expose)

    [:octicons-arrow-right-24: Debugger Documentation](commands.md)

- :fontawesome-brands-usb: Inspect device states

    ---
    - Motor information
    - Battery power
    - Connected remote information
    - Radio I/O

    [:octicons-arrow-right-24: C++ Documentation](macros.md#FIXME_TODO)

    [:octicons-arrow-right-24: Debugger Documentation](commands.md)

</div>

??? warning "Limitations of v5dbg"
    - **Every function must begin with `$function`**
    - **Variables accessible by the debugger must be fed into `$expose`**
    - **If your program has a fatal crash v5dbg cannot suspend the program.**
    - **Line-by-line stepping is not possible**
