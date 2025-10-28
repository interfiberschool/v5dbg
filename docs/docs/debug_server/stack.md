# Stack traces

## Limitations

Unlike debuggers for desktop operating system which can request backtraces using system calls such as [backtrace(3)](https://man7.org/linux/man-pages/man3/backtrace.3.html), neither **PROS** or **VexOS** offer a way to obtain such information from the user program.

## Our Solution

C++ offers a feature to classes called **destructors** which do the opposite of their **constructor** and usually ends up freeing resources. 

v5dbg uses these to its advantage with the `V5DbgFunction` class. When this class is **constructed** its fed in location information obtained from the `__PRETTY__FUNCTION__`, `__FILE__`, and `__LINE__` macros. In the constructor we access the current virtual callstack vector for our thread and push all this debug info into it at **the last index**.

The C++ compiler will automatically call the destructor once this class instance falls out of scope in the **current function**, inside our destructor we call `pop_back` on the current virtual callstack vector.

With this method, a function's debug information is inserted onto the virtual callstack at the **proper location** and is available for the **entire duration of its execution**. When we wish to inspect the callstack, like for [`DEBUGGER_MESSAGE_VSTACK_FOR`](/protocol/v1/#debugger_message_vstack_for) messages, we simply loop through the proper callstack vector.

Since collecting debug info and constructing classes is annoying to do manually for every function its been compressed into a **singular macro** called [`$function`](/cpp/macros/debug/function), when this macro is used at the top of a function it **generates the code** required to generate stack traces and places the `V5DbgFunction` class instance in a local variable named `_v5dbg_stack_func`

## Future Alternatives

In the future **libunwind** could be used to obtain a backtrace without the use of [`$function`](/cpp/macros/debug/function). Since `libunwind` only returns addresses it would be up to the debugger to convert them into human readable locations with tools such as `addr2line`.
