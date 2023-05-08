# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
from maya import cmds, mel

####################################################################################################
# Do not change the following variables.
_MODULE_NAME_PLACEHOLDER = "<MODULE_NAME>"
_MODULE_VERSION_PLACEHOLDER = "<MODULE_VERSION>"
_MODULE_DIR_PATH_PLACEHOLDER = "<MODULE_DIR_PATH>"
_SCRIPT_DIR_PATH_PLACEHOLDER = "<SCRIPT_DIR_PATH>"

_DEFAULT_MEL_ICON_NAME = "commandButton.png"
_DEFAULT_PYTHON_ICON_NAME = "pythonFamily.png"
####################################################################################################
# Please replace the following variables with your own.
# About module file
# ex) _MODULE_FILE_NAME = "myModule.mod"
# ex) _MODULE_NAME = "myModule"
# ex) _MODULE_VERSION = "1.0.0"
# ex) _MODULE_DIR_PATH = "modules"
# ex) _SCRIPT_DIR_PATH = "scripts"

# About shelf button
# ex) _COMMAND = """
# import my_module
# my_module.main()
# """
# ex) _ICON_DIR_RELATIVE_PATH = "icons"
# ex) _ICON_FILE_NAME = "myModule.png"
# ex) _SOURCE_TYPE = "python"
####################################################################################################
# About module file
_MODULE_FILE_NAME = "<your module file name>.mod"
_MODULE_NAME = "<your module name>"
_MODULE_VERSION = "<your module version>"
_MODULE_DIR_PATH = "<your module directory path>" # default: "modules"
_SCRIPT_DIR_PATH = "<your script directory path>" # default: "scripts"

# About shelf button
_COMMAND = """
<your command>
"""
_ICON_DIR_PATH = "<your icon directory path>" # default: "icons"
_ICON_FILE_NAME = "<your icon file name>" # default: "commandButton.png" or "pythonFamily.png"
_SOURCE_TYPE = "python" # "mel" or "python"
####################################################################################################

def onMayaDroppedPythonFile(*args, **kwargs):
    """This function is called when the user drops this file into the Maya viewport."""
    if not _distribute_mod_file():
        # If the installation fails, do not register the command to the shelf.
        return
    # If the installation succeeds, register the command to the shelf.
    _register_command_to_shelf()

def _distribute_mod_file():
    """Distribute the module file to the default module directory."""
    root_path = os.path.dirname(os.path.abspath(__file__))
    maya_module_paths = mel.eval("getenv MAYA_MODULE_PATH")
    user_app_dir_path = cmds.internalVar(userAppDir=True)
    maya_version = cmds.about(version=True)[:4]
    default_module_dir_path = os.path.join(user_app_dir_path, maya_version, "modules")
    default_module_dir_path = default_module_dir_path.replace(os.sep, "/")
    template_module_dir_path = os.path.join(root_path, _MODULE_DIR_PATH)
    template_module_file_path = os.path.join(template_module_dir_path, _MODULE_FILE_NAME)

    if default_module_dir_path not in maya_module_paths:
        cmds.error("\"{0}\" install failed. \"{1}\" is not in MAYA_MODULE_PATH.".format(_MODULE_NAME, default_module_dir_path))
        return False

    if not os.path.exists(default_module_dir_path):
        os.makedirs(default_module_dir_path)

    scripts_dir_path = os.path.join(root_path, _SCRIPT_DIR_PATH)
    if not os.path.exists(scripts_dir_path):
        cmds.error("\"{0}\" install failed. \"{1}\" does not exist.".format(_MODULE_NAME, scripts_dir_path))
        return False

    if scripts_dir_path not in sys.path:
        sys.path.append(scripts_dir_path)
        print("\"{0}\" installed to sys.path successfully.".format(scripts_dir_path))

    with open(template_module_file_path, "r") as f:
        template_module_file_content = f.read()

    template_module_file_content = template_module_file_content.replace(_MODULE_NAME_PLACEHOLDER, _MODULE_NAME)
    template_module_file_content = template_module_file_content.replace(_MODULE_VERSION_PLACEHOLDER, _MODULE_VERSION)
    template_module_file_content = template_module_file_content.replace(_MODULE_DIR_PATH_PLACEHOLDER, root_path)
    relative_script_dir_path = os.path.relpath(scripts_dir_path, template_module_dir_path)
    template_module_file_content = template_module_file_content.replace(_SCRIPT_DIR_PATH_PLACEHOLDER, relative_script_dir_path)
    module_file_content = template_module_file_content

    module_file_path = os.path.join(default_module_dir_path, _MODULE_FILE_NAME)

    with open(module_file_path, "w") as f:
        f.write(module_file_content)

    print("\"{0}\" installed to \"{1}\" successfully.".format(_MODULE_NAME, default_module_dir_path))

    return True

def _register_command_to_shelf(module_name=_MODULE_NAME, icon_dir_path=_ICON_DIR_PATH, icon_file_name=_ICON_FILE_NAME, annotation=_MODULE_NAME, command=_COMMAND, label=_MODULE_NAME, source_type=_SOURCE_TYPE):
    root_path = os.path.dirname(os.path.abspath(__file__))
    icon_file_path = os.path.join(root_path, icon_dir_path, icon_file_name)
    if icon_file_name == _DEFAULT_MEL_ICON_NAME or icon_file_name == _DEFAULT_PYTHON_ICON_NAME:
        icon_file_path = icon_file_name
    else:
        if not os.path.exists(icon_file_path):
            cmds.error("\"{0}\" install failed. \"{1}\" does not exist.".format(module_name, icon_file_path))
            return

    active_shelf_name = cmds.shelfTabLayout("ShelfLayout", query=True, selectTab=True)
    active_shelf_buttons = cmds.shelfLayout(active_shelf_name, query=True, childArray=True)

    button_to_register = None
    if active_shelf_buttons:
        for button in active_shelf_buttons:
            if cmds.shelfButton(button, query=True, label=True) == module_name:
                button_to_register = button
                break

    if button_to_register:
        cmds.shelfButton(button_to_register, edit=True, command=command)
    else:
        cmds.shelfButton(
            annotation=annotation,
            command=command,
            image=icon_file_path,
            label=label,
            parent=active_shelf_name,
            sourceType=source_type,
        )

    print("\"{0}\" install success.".format(_MODULE_NAME))
