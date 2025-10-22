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

    pros::lcd::print(0, "%s", s);
}

void opLoop()
{
    $function

    printData("Hello World");

    pros::delay(300);
}

void
opcontrol(void)
{
    $ntask
    $function

    int x = 0;

    std::vector<int> data;
    $expose(data);

    std::vector<double> dataHist;
    $expose(dataHist);

    while (true)
    {
        int test = x * 2;
        $expose(test);

        double other = x * 2.344;
        $expose(other);

        std::string myName = "Hunter - Lead programer for 8568T";
        $expose(myName);

        data.push_back(x);
        dataHist.push_back(other);

        printf("%i\n", x);

        opLoop();

        pros::lcd::print(1, "%i", x);

        x++;
    }
}
