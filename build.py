"""Build script for creating executable with PyInstaller"""
import PyInstaller.__main__
import os
import shutil

# Clean previous builds
if os.path.exists("build"):
    shutil.rmtree("build")
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("competitionmonitor.spec"):
    os.remove("competitionmonitor.spec")

# PyInstaller arguments
separator = ";" if os.name == "nt" else ":"
args = [
    "run_desktop.py",
    "--name=competitionmonitor",
    "--onefile",
    "--windowed",  # No console window
    "--icon=NONE",  # You can add an icon file if available
    f"--add-data=config.py{separator}.",  # Include config.py
    "--hidden-import=PyQt6.QtCore",
    "--hidden-import=PyQt6.QtGui",
    "--hidden-import=PyQt6.QtWidgets",
    "--hidden-import=selenium",
    "--hidden-import=openai",
    "--hidden-import=requests",
    "--collect-all=webdriver_manager",
    "--collect-all=selenium",
]

print("Building executable...")
PyInstaller.__main__.run(args)

print("\nBuild complete!")
print("Executable location: dist/competitionmonitor.exe")

