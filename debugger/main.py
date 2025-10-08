from subprocess import Popen, PIPE, STDOUT
import time
import sys

print("# Connecting to remote debug server via USB SERIAL")

term = Popen(['C:\\Users\\Student\\AppData\\Roaming\\Code\\User\\globalStorage\\sigbots.pros\\install\\pros-cli-windows\\pros.exe', 'terminal'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, text=True)
time.sleep(1) # TODO: Wait for OPEN

while True:
  cmd = input("] ")

  if cmd == "suspend":
    term.stdin.write(b"%1:1:0\n")
    term.stdin.flush()