# `frame`

!!! abstract "Command information"
    Regular name **`frame`** :octicons-unlink-24:

    Introduced in version **v0.1** :octicons-tag-24:

## About

The `frame` command is used to change the frame the debugger is inspecting on the [callstack](./backtrace.md)

## Syntax

When invoked with **no arguments** this command prints out the current frame ID.

When invoked with a **single integer** argument this command changes the frame ID to the argument and prints out the new active frame state.
