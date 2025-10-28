# Exposed memory

## Limitations

Exposing memory **would be** easy if PROS provided a better way to capture debug information and read it at runtime. On Linux systems debug info for executables is usually stored in the **DWARF** format and is used by debuggers to find the addresses of variables along with information on data types and functions.

## Our Solution

### Memory Types and the Type Database

v5dbg has a list of predefined, but extendable, **memory types**. Since memory types are just enums they do not directly convert into C++ types.

In order to convert a C++ type into a `v5dbg_memory_type_e` we use the **type database** which stores the `hash_code` of a [`std::type_info`](https://en.cppreference.com/w/cpp/types/type_info.html) as the **key** and the memory type as the **value**.

### `$expose` macro

The [`$expose`](/cpp/macros/debug/expose) macro takes in a variable and allows it to be **exposed** to the debugger. When `$expose` is invoked it generates code to register a `void*` to the variable with the debug server along with any **type information** which is obtained with the [`typeid`](https://www.cppreference.com/w/cpp/language/typeid.html) operator.

When the `$expose` macro falls **out of scope** it automatically marks the variable as *deallocated* with the debug server. More information on how actual reading of variable memory can be found in the [pretty printers](../advanced/pretty_printers.md) section.
