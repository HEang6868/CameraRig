#From Mehveesh Nida

import maya.cmds as cmds
import os

def onMayaDroppedPythonFile(*args):
    """
    Called automatically when this file is dragged & dropped into Maya viewport.
    Creates a shelf button that runs a script.
    """
    shelf_name = "Custom"  # Change to existing shelf name if you like
    button_label = "Camera Rig"
    tooltip = "Creates a rigged camera."
    icon_name = "CameraRigIcon.png"  # Your custom icon file name

    # Find icon path (assumes icon is next to this .py file)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, icon_name)

    # Confirm shelf exists
    if not cmds.shelfLayout(shelf_name, exists=True):
        print(f"Shelf '{shelf_name}' not found. Please create it or change to an existing shelf (e.g., 'Polygons').")
        return

    #remove existing button with same label
    children = cmds.shelfLayout(shelf_name, query=True, childArray=True) or []
    for child in children:
        if cmds.shelfButton(child, query=True, label=True) == button_label:
            cmds.deleteUI(child)

    # Command that will run your tool when the button is clicked
    cmd = 'import CameraRig.CameraRig as camRig; camRig.make_camera_rig()'

    # Add the button to the shelf
    cmds.shelfButton(
        label=button_label,
        parent=shelf_name,
        command=cmd,
        sourceType="Python",
        annotation=tooltip,
        image=icon_path  # use your icon, must be in prefs/icons or an accessible path
    )

    cmds.inViewMessage(amg=f"<hl>{button_label}</hl> added to <hl>{shelf_name}</hl> shelf!", pos='topCenter', fade=True)
