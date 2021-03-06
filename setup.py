#!/usr/bin/python3
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
                     "packages": ["os","pygments","pygments.lexers","pygments.formatters", 'numpy.core._methods', 'numpy.lib.format', "pyqtgraph"], 
                     "excludes": ["tkinter"],
                     "include_files":['README.md', 'sample.log', 'siraj_configs.json']
                     }
# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "siraj",
        version = "1.1",
        description = "Siraj",
        options = {"build_exe": build_exe_options},
        executables = [Executable("siraj.py", base=base)])
