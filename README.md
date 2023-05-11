# Maya Drag and Drop Installer

[Japanese](README-ja.md)

This repository contains scripts that allow you to easily create an installer for your Maya tools that users can install by simply dragging and dropping a file into Maya.

## Environment

- Windows 10
- Maya 2020

## Installation

1. Download the [latest release](https://github.com/NinaMina2737/maya-drag-and-drop-installer/releases/latest) and extract the archive.

## Requirements

Before using this tool, please make sure to satisfy the following requirements:

- You need to put all the script directories and files for your tool into one directory to designate the script directory for this tool.

## Usage

1. Run `installer_generator.bat` and follow the prompts to generate the installer script (`new_installer.py`).
2. Move the generated `new_installer.py` script into the same directory as your Maya tool script directory.
3. Distribute the `new_installer.py` script along with your tool script files.
4. Users can now install your tools by dragging and dropping the `new_installer.py` file into Maya.

**Note:** Be careful where you place the completed installer, and be careful with the script directory you specify. When the installer is executed, the commands you set in the installer will be registered in the currently active shelf.

## Customization

You can also create a custom installer by directly editing the constants in `maya_drag_and_drop_installer.py`.

### About module file

- `_MODULE_FILE_NAME`: The name of the module file to be created.
- `_MODULE_NAME`: The name of the module.
- `_MODULE_VERSION`: The version of the module.
- `_SCRIPTS_DIR_NAME`: The name of the directory that contains your tool script files.

### About shelf button

- `_COMMAND`: The command to be executed when the user clicks the shelf button.
- `_ICON_DIR_NAME`: The name of the directory that contains the icon file for the shelf button.
- `_ICON_FILE_NAME`: The name of the icon file for the shelf button. By default, the script uses `commandButton.png` for MEL scripts and `pythonFamily.png` for Python scripts.
- `_SOURCE_TYPE`: The type of the script file. This can be either `"mel"` or `"python"`.

## Troubleshooting

- If the installation fails, the command will not be registered to the shelf.
- If you encounter issues with the installation, check that the path to the script directory is correct and that the module file is being created in the correct location.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
