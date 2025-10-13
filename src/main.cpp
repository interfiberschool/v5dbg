#include "main.h"
#include "liblvgl/llemu.hpp"
#include "pros/llemu.hpp"
#include "v5dbg/debug.h"
#include "v5dbg/server.h"

v5dbg_server_state_t sState{};

void
autonomous(void)
{
}

void
initialize(void)
{
    sState = V5Dbg_AllocateServerState();

    V5Dbg_StartServer(&sState);

    pros::lcd::initialize();
}

void
disabled(void)
{
}

void
competition_initialize(void)
{
}

void printData(const char* s)
{
    $function

    $expose(s);

    pros::lcd::print(1, "%s", s);
}

void opLoop()
{
    $function

    printData("Hello World");
}

void
opcontrol(void)
{
    $ntask
    $function

    while (true)
    {
        int test = 100;
        $expose(test);

        opLoop();

        pros::delay(300);
    }
}
