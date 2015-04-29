#!/bin/bash

# Step_01 - Freeze current code
python3 setup.py build


# Step_02 - Compress the frozen folder
mkdir -p release/linux/siraj_linux
cp -r build/exe.linux-x86_64-3.4/* release/linux/siraj_linux/
cd release/linux/
tar cfz siraj_linux.tar.gz siraj_linux
cd ../../


# Step_03 - Cleanup
rm -rf release/linux/siraj_linux
rm -rf build

