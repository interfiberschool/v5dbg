$env:Path += ";/Users/Student/AppData/Roaming/Code/User/globalStorage/sigbots.pros/install/pros-cli-windows"
$env:Path += ";C:\Users\Student\AppData\Roaming\Code\User\globalStorage\sigbots.pros\install\pros-toolchain-windows\usr\bin"
$env:Path += ";C:\Users\Student\AppData\Roaming\Code\User\globalStorage\sigbots.pros\install\vex-vexcom-windows"

make -j
pros upload
pros v5 run
python3 debugger\main.py