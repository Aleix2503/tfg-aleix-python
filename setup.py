#!/usr/bin/env python3
"""
Setup script for FSM Editor Framework
Builds an executable and registers file associations for .fsmproj files
"""

import subprocess
import sys
import os
from pathlib import Path

def build_executable():
    """Build the executable using PyInstaller"""
    # Get the directory of this script
    project_dir = Path(__file__).parent
    main_py = project_dir / "main.py"

    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=FSMEditor",
        "--onefile",
        "--windowed",
        # "--icon=fsm_icon.ico",  # Optional: add icon if you have one
        "--add-data=data:data",  # Include data folder
        "--add-data=model:model",  # Include model folder
        "--add-data=editor:editor",  # Include editor folder
        "--add-data=commands:commands",  # Include commands folder
        "--add-data=persistence:persistence",  # Include persistence folder
        "--add-data=export:export",  # Include export folder
        str(main_py)
    ]

    try:
        result = subprocess.run(cmd, cwd=str(project_dir), check=True)
        exe_path = project_dir / "dist" / "FSMEditor.exe"
        if exe_path.exists():
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        return False
    except FileNotFoundError:
        return False

def register_file_association(exe_path):
    """Register .fsmproj files to open with the FSM Editor"""

    # Ensure exe_path is absolute
    exe_path = str(Path(exe_path).resolve())

    # Windows registry commands
    registry_commands = [
        # Create file association for .fsmproj
        f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.fsmproj\\UserChoice" /f',

        # Register file type
        f'reg add "HKCR\\.fsmproj" /ve /d "FSMProjectFile" /f',
        f'reg add "HKCR\\.fsmproj" /v "Content Type" /d "application/x-fsmproj" /f',

        # Register program
        f'reg add "HKCR\\FSMProjectFile" /ve /d "FSM Project File" /f',
        f'reg add "HKCR\\FSMProjectFile\\DefaultIcon" /ve /d "{exe_path},0" /f',
        f'reg add "HKCR\\FSMProjectFile\\shell\\open\\command" /ve /d "\"{exe_path}\" \"%%1\"" /f',
    ]

    success = True
    for cmd in registry_commands:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, check=False)
                # Continue anyway, some commands might fail due to permissions
        except Exception as e:
            pass

    return True

def main():
    """Main setup routine"""
    # Check if we're on Windows
    if sys.platform == "win32":
        # Build executable
        if not build_executable():
            return False

        # Register file association
        exe_path = Path(__file__).parent / "dist" / "FSMEditor.exe"
        if exe_path.exists():
            register_file_association(str(exe_path))
        else:
            return False

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
