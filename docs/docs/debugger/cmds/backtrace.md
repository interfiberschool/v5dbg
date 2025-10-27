# `backtrace`

!!! abstract "Command information"
    Regular name **`backtrace`** :octicons-unlink-24:

    Other names **`bt`**, **`stack`** :octicons-link-24:

    Introduced in version **v0.1** :octicons-tag-24:

## About

The `backtrace` command is used to obtain the current callstack of the **suspended** program's selected [thread](./thread.md).

## Notes

!!! warning
    This command will only print a stacktrace when the program is in the `SUSPEND` state.

## Syntax

This command accepts **no arguments**.
