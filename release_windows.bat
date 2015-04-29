#cd c:/Users/Mohamed/git/siraj/release/windows
#
## Delete previous release file
#del siraj_windows.zip
#
## Freeze the application
#cd c:\Python34\Scripts
#python cxfreeze "c:/Users/Mohamed/git/siraj/siraj.py" --target-dir c:\Users\Mohamed\git\siraj\release\windows\siraj_windows
#
#cd
#rmdir siraj_windows /s /q


# Step_01 - Freeze current code
python setup.py build


# Step_02 - Compress the frozen folder
mkdir release/windows/siraj_windows
copy build/exe.win32-3.4/* release/windows/siraj_windows/
cd release/windows/
#tar cfz siraj_linux.tar.gz siraj_linux
cd ../../


# Step_03 - Cleanup
#rm -rf release/linux/siraj_linux
#rm -rf build

