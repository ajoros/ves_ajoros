from setuptools import find_packages
import sys

from cx_Freeze import Executable, setup

print(find_packages())
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = "Water4 VES Inverse Analysis",
      version = "0.1",
      description = (
          'Softare application to determine depth to water using vertical ' +
          'electical sounding.'),
      packages=find_packages(),
      # options = {"build_exe": build_exe_options},
      executables = [Executable(
        'ves/main.py', base=base, packages=find_packages())])
