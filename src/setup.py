import sys
import os
import PyQt5
from cx_Freeze import setup, Executable

platform_plugin_path = os.path.join(os.path.dirname(PyQt5.__file__), 'Qt5', 'plugins', 'platforms')

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platform_plugin_path

icon_path = "images/icon.ico"
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
build_exe_options = {
    "packages": ["os", "sys", "PyQt5"],
    "include_files": [
        (platform_plugin_path, "platforms"),
          ('images','images'),
          'stream.json',
          icon_path,
    ],
    "excludes": ["PyQt5.QtQml"] 
}


setup(
    name="PMS",
    version="1.0",
    description="Pupil Management System",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/main.py",init_script=None, base=base,target_name='Admin.exe'),Executable("src/teachers_panel.py",init_script=None,base=base,target_name='Teacher.exe'),Executable("src/SQL.py",init_script=None,target_name="SQL_EDITOR.exe",icon=icon_path)]
)
