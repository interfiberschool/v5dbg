# Commands
Documentation for all debugger commands and their options

## `backtrace`, or `bt`
Print the generated backtrace obtained using [$function](./macros.md#function) macro locations.

```
] backtrace
(0) void opcontrol() at src/main.cpp:54 -> 0x125830076
```

### Notes
* The jump address listed is the jump location of the [$function](./macros.md#function) call, not the actual function.

## `frame [FRAME_ID]`
Goto the given frame ID in the backtrace.

```
] frame 0
# SELECTED FRAME 0 at src/main.cpp:54
```

## `thread`
List all supervised threads and their IDs.

```
] thread
(0) User Operator Control (PROS)
(1) Odom System
```

## `thread [ID]`
Change the active thread to be operating on.

```
] thread 1
# THREAD CHANGED TO "Odom System" ID OF #1
```

## `scope local`
Print all exposed local memory and it's state.

```
] scope local

float x = <UNALLOCATED>;
  Allocation tagged at src/main.cpp:567

float y = 52;
  Allocated tagged at src/main.cpp:566
```

### Notes
* If a variable is marked as `UNALLOCATED` the program has not reached its allocation point but knows that it has been allocated before.

## `scope global`
Print all exposed global memory and it's state.

```
TODO
```

## `suspend`, or `pause`
Pauses all supervised tasks.

```
] suspend
# SUSPENDED ALL SUPERVISED TASKS
```

## `resume`, or `continue`
Resumes all supervised tasks from their suspended state.

```
] resume
# RESUMED ALL SUPERVISED TASKS
```

## `print [VARIABLE]`
Print the value of a variable using its pretty printer, if not pretty printer is found it will default to a `void*`.

```
] print y
float y = 52;

] print myCustomClass
void* myCustomClass = 0x453;

] print myOtherClass
void* myOtherClass = 0x0 (unallocated);
```

### Notes
* Printing unallocated variables will result in `0x0 (unallocated)`
* Variable names must belong to the global or local stack frame scope
* Variables must be exposed with [$expose](macros.md#exposet)

## `set [KEY] [VAL]`
Set the temporary value for the given variable, the value of the variable is interpreted by the pretty printer, if no pretty printer is found this will fail.

```
] print y
float y = 52;

] set y 72
# SET VARIABLE 'y' to 52

] print y
float y = 72;
```

### Notes
* As stated above the value of the variable is set by the pretty printer, without a valid pretty printer this function will fail. See [setp](#setp-key-pointer) to set the value of a pointer.

## `setp [KEY] [POINTER]`
Set the raw memory address of a pointer object.

```
] print myClass
void* myClass = 0x0;

] setp myClass 0x5b23
# POINTER VALUE FOR 'myClass' SET TO 0x5b23
```

### Notes
* `setp` does not yet work on smart pointers such as `std::shared_ptr`, `std::unique_ptr`, or `std::weak_ptr`