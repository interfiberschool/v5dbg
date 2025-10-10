# 8568T's V5 Debugger
V5dbg is an experimental realtime debugger for the V5 brain

## What can v5dbg do?
- Set software breakpoints
    - Set breakpoints on function entrance/exit, memory allocations, and manual locations
    - Conditional breakpoints
- Inspect active threads
    - View active locks and which threads hold them
    - View the generated callstack for a thread at any time
    - Easily switch the debuggers active context to another thread
- Inspect, set, and manage memory
    - Automatically pretty print variables based on compile-time type information
    - Set memory value to a constant, variable constant, or temporary value.
        - Constant set = Every time this variable is allocated set it to `x`
        - Variable constant = Every time this variable is allocated with `y` change it to `x`
        - Temporary value = Set this variable to `x` when reallocation occurs it willl change back to `y`
- Inspect device states
    - Motor information
    - Battery power
    - Connected remote information
    - Radio I/O

## Limitations of v5dbg
- Every function must begin with `$function`
- Variables accessible by the debugger must be fed into `$expose`
- If your program has a fatal crash v5dbg cannot suspend the program.
- Line-by-line stepping is not possible