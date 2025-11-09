#!/usr/bin/env bash

export PATH=$PATH:~/.config/Code/User/globalStorage/sigbots.pros/install/pros-toolchain-linux/bin/:~/.config/Code/User/globalStorage/sigbot.pros/install/pros-cli

make -j
pros upload
