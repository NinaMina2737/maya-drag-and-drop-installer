@echo off
setlocal enabledelayedexpansion

set "TEMPLATE_SCRIPT_NAME=maya_drag_and_drop_installer_template.py"
set "NEW_SCRIPT_NAME=new_installer.py"
set "TEMPLATE_SCRIPT_PATH=%~dp0%TEMPLATE_SCRIPT_NAME%"
set "NEW_SCRIPT_PATH=%~dp0%NEW_SCRIPT_NAME%"

if exist "%NEW_SCRIPT_PATH%" (
    echo Script file already exists. Please delete or move it and try again.
    exit /b 1
)

copy "%TEMPLATE_SCRIPT_PATH%" "%NEW_SCRIPT_PATH%"

if not exist "%NEW_SCRIPT_PATH%" (
    echo Failed to create new script file.
    exit /b 1
)

:ReplaceModuleFileName
set /p "VALUE=Please enter the value for MODULE_FILE_NAME: "
if /i "!VALUE!"=="" (
  echo Invalid module file name. Please try again.
  goto :ReplaceModuleFileName
) else (
  call :ReplaceConstants "<your module file name>" "!VALUE!"
)

:ReplaceModuleName
set /p "VALUE=Please enter the value for MODULE_NAME: "
if /i "!VALUE!"=="" (
  echo Invalid module name. Please try again.
  goto :ReplaceModuleName
) else (
  call :ReplaceConstants "<your module name>" "!VALUE!"
)

:ReplaceModuleVersion
set /p "VALUE=Please enter the value for MODULE_VERSION: "
if /i "!VALUE!"=="" (
  echo Invalid module version. Please try again.
  goto :ReplaceModuleVersion
) else (
  call :ReplaceConstants "<your module version>" "!VALUE!"
)

:ReplaceModuleDirectoryName
set /p "VALUE=Please enter the value for MODULE_DIR_NAME: "
if /i "!VALUE!"=="" (
  echo Invalid module directory name. Please try again.
  goto :ReplaceModuleDirectoryName
) else (
  call :ReplaceConstants "<your module directory name>" "!VALUE!"
)

:ReplaceScriptsDirectoryName
set /p "VALUE=Please enter the value for SCRIPTS_DIR_NAME: "
if /i "!VALUE!"=="" (
  echo Invalid scripts directory name. Please try again.
  goto :ReplaceScriptsDirectoryName
) else (
  call :ReplaceConstants "<your scripts directory name>" "!VALUE!"
)

:ReplaceCommand
set "COMMAND_NEW_LINE_PLACEHOLDER=<COMMAND_NEW_LINE>"
set "VALUE="
echo "Enter the value for COMMAND (press Ctrl+Z and Enter when done):"
for /f "delims=" %%i in ('type con') do (
  set "VALUE=!VALUE!%%i!COMMAND_NEW_LINE_PLACEHOLDER!"
)
if "!VALUE!"=="" (
  echo Invalid command. Please try again.
  goto :ReplaceCommand
) else (
  call :ReplaceConstants "<your command>" "!VALUE!"
)

:ReplaceSourceType
set /p "VALUE=Which source type do you want to use? (m/p): "
if /i "!VALUE!"=="m" (
  set "SOURCE_TYPE=mel"
) else if /i "!VALUE!"=="p" (
  set "SOURCE_TYPE=python"
) else (
  echo Invalid source type. Please try again.
  goto :ReplaceSourceType
)
call :ReplaceConstants "<your source type>" "!SOURCE_TYPE!"

:ReplaceIconData
set "DEFAULT_ICON_DIR_NAME=icons"
set "DEFAULT_ICON_FILE_NAME=commandButton.png"
if /i "%SOURCE_TYPE%"=="python" (
    set "DEFAULT_ICON_FILE_NAME=pythonFamily.png"
)
set /p "USE_DEFAULT_ICON=Do you want to use the default icon file (%DEFAULT_ICON_FILE_NAME%) for this script? (y/n): "
if /i "!USE_DEFAULT_ICON!"=="y" (
    set "ICON_DIR_NAME=%DEFAULT_ICON_DIR_NAME%"
    set "ICON_FILE_NAME=%DEFAULT_ICON_FILE_NAME%"
) else (
    set /p "ICON_DIR_NAME=Please enter the icon directory name (press Enter for default name: %DEFAULT_ICON_DIR_NAME%): "
    set /p "ICON_FILE_NAME=Please enter the icon file name (including extension): "
    if not defined ICON_DIR_NAME set "ICON_DIR_NAME=%DEFAULT_ICON_DIR_NAME%"
    if ICON_FILE_NAME=="" (
        echo Invalid icon file name. Please try again.
        goto :ReplaceIconData
    )
)
set "VALUE=%ICON_DIR_NAME%"
call :ReplaceConstants "<your icon directory name>" "!VALUE!"
set "VALUE=%ICON_FILE_NAME%"
call :ReplaceConstants "<your icon file name>" "!VALUE!"
goto :eof

:ReplaceConstants
set "SEARCH=%~1"
set "VALUE=%~2"
set "VALUE=!VALUE:'=^'!"
set "VALUE=!VALUE:"=^"!"
set "VALUE=!VALUE:%%=^%%!"
powershell -command "(Get-Content '%NEW_SCRIPT_PATH%') -replace '!SEARCH!', '!VALUE!' | Set-Content '%NEW_SCRIPT_PATH%'"
goto :eof
