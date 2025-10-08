#include "main.h"
#include "v5dbg/debug.h"
#include "v5dbg/server.h"

void
on_center_button()
{
}

v5dbg_server_state_t serverState{};

void
initialize()
{
  serverState = V5Dbg_AllocateServerState();

  V5Dbg_StartServer(&serverState);
}

void
disabled()
{
}

void
competition_initialize()
{
}

void
autonomous()
{
}

void
printData(const std::string& d)
{
  $function

    printf("%s\n", d.c_str());
}

void
run()
{
  $function

    pros::delay(200);
  printData("Hello World");
}

void
opcontrol()
{
  V5Dbg_Init();
  $function

  pros::lcd::initialize();

  int x = 0;
  while (true)
  {
    run();

    pros::lcd::print(0, "%i", x);

    pros::delay(20);

    x++;
  }
}
