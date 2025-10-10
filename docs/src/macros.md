# Macros
All macros should be defined in the `v5dbg/debug.h` header file, **make sure to include this!**

## `$function`
Makes the currently scoped function debuggable.

**NOTE**: Without this function 99% of program debugging functions will not work, and this frame will be hidden from stack traces.

#### Example

```c++
// Some dummy functions to demonstrate $function

/**
 * Set the drivetrain voltage
 * @param power Power in volts
*/
void
driveVoltage(int power)
{
    $function

    driveTrain->setVoltage(power);
}

void
driveTime(int ms)
{
    $function // Make sure we appear in stack traces and stuff!

    // Drive forward at 20 volts for `ms` time
    driveVoltage(20);

    pros::delay(ms);

    driveVoltage(0); // Reset power after sleep
}
```

## `$ntask`
Informs the debugger of a new task to supervise, this should be the first line of code within every function.

**NOTE**: When `$ntask` falls out of scope the task is automatically dropped from the debugger making it undebuggable.

#### Example
```c++
void
opcontrol()
{
    $ntask // Operator control task was spawned by the PROS system daemon, make sure the debugger knows this

    while (true)
    {
        // .. opcontrol stuff .. 

        pros::delay(20); // Allow RTOS to perform a context switch
    }
}
```

## `$expose`
Expose a scoped variable to the debug server for inspection.

#### Example
```c++
void
opcontrol()
{
    int fwdVoltage = 200;
    $expose(fwdVoltage); // Expose the fwdVoltage variable to the debugger, the $expose macro will automatically get type information for us & the pretty printer

    while (true)
    {
        if (ButtonPressed(BUTTON_X))
        {
            driveVoltage(fwdVoltage);
        }
        else
        {
            driveVoltage(0);
        }
    }
}
```