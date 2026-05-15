@echo off
REM FSM Project File Association Registration Script
REM This batch file registers .fsmproj files to open with FSM Editor
REM Run as Administrator for best results

setlocal enabledelayedexpansion

echo.
echo ====================================================
echo FSM Editor - File Association Setup
echo ====================================================
echo.

REM Get the directory where the batch file is located
set SCRIPT_DIR=%~dp0
set EXE_PATH=%SCRIPT_DIR%dist\FSMEditor.exe

REM Check if executable exists
if not exist "!EXE_PATH!" (
    echo Error: FSMEditor.exe not found at !EXE_PATH!
    echo.
    echo Please run setup.py first to build the executable:
    echo   python setup.py
    echo.
    pause
    exit /b 1
)

echo Found executable: !EXE_PATH!
echo.
echo Registering .fsmproj file extension...
echo.

REM Replace backslashes with double backslashes for registry
set REG_EXE_PATH=!EXE_PATH:\=\\!

REM Create temporary registry file
set TEMP_REG=%TEMP%\fsmproj_register.reg
(
    echo Windows Registry Editor Version 5.00
    echo.
    echo ; FSM Project File Association
    echo [HKEY_CLASSES_ROOT\.fsmproj]
    echo @="FSMProjectFile"
    echo "Content Type"="application/x-fsmproj"
    echo.
    echo [HKEY_CLASSES_ROOT\FSMProjectFile]
    echo @="FSM Project File"
    echo.
    echo [HKEY_CLASSES_ROOT\FSMProjectFile\DefaultIcon]
    echo @="!REG_EXE_PATH!,0"
    echo.
    echo [HKEY_CLASSES_ROOT\FSMProjectFile\shell\open\command]
    echo @="\"!REG_EXE_PATH!\" \"%%1\""
) > "!TEMP_REG!"

REM Apply registry file
reg import "!TEMP_REG!"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================================
    echo SUCCESS: File association registered!
    echo ====================================================
    echo.
    echo You can now:
    echo   - Double-click .fsmproj files to open them
    echo   - Run FSMEditor.exe directly from:
    echo     !EXE_PATH!
    echo.
) else (
    echo.
    echo Error: Failed to register file association
    echo You may need to run this script as Administrator
    echo.
)

REM Clean up
if exist "!TEMP_REG!" del "!TEMP_REG!"

pause
