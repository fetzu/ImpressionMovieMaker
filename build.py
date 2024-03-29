import sys
from cx_Freeze import setup, Executable
from ImpressionMovieMaker import VERSION

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["soundfile"], "include_files": [("sndfile.dll","./lib/sndfile.dll")], "optimize": 1}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "ImpressionMovieMaker",
    version = VERSION,
    description = f"ImpressionMovieMaker v{VERSION} !",
    options = {"build_exe": build_exe_options},
    executables = [Executable("ImpressionMovieMaker.py", base=base, icon="assets/icon_alt.ico")]
)