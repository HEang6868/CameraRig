import maya.cmds as mc


#Point values for custom control shapes.
CAM_CTRL_PNTS = [[3.0, 0.0, -3.0], [0.0, 0.0, 15.03715], [-3.0, 0.0, -3.0], 
                 [-5.0, 0.0, -0.0], [-6.0, -0.0, 8.0], [-0.0, -0.0, 11.0], 
                 [6.0, -0.0, 8.0], [5.0, -0.0, 0.0]]

AIM_CTRL_PNTS = [[-4.13308, 1.56759, 3.549], [-3.95377, 1.56759, 8.86711], [0.07047, 1.56759, 10.08455], 
                 [3.37513, 1.56759, 8.64562], [4.10616, 1.56759, 4.0668], [0.04215, 1.56759, -1.64912], 
                 [0.04215, 1.56759, -1.64912], [-0.10454, 1.56759, -1.64912], [-0.10454, 1.56759, -1.64912],
                   [-0.10454, 1.56759, -1.64912], [-0.10454, 1.56759, -1.64912], [-0.10454, 1.56759, -1.64912], 
                   [-0.10454, 1.56759, -1.64912], [-0.10454, 1.56759, -1.64912]
                   ]
TARGET_PNTS = [[0.00012, 1.36504, -0.04559], [0.0, 1.28835, -1.17191], [0.0, 0.0, -1.73424], 
               [0.0, -1.12465, -1.17191], [0.0, -1.68698, -0.04726], [0.0, -1.12465, 1.07739], 
               [0.0, 0.0, 1.63972], [0.0, 1.28835, 1.07739], [-0.0012, 1.36509, -0.04661], 
               [0.0012, 1.36505, -0.04893], [1.12769, 1.28227, -0.04726], [1.68698, 0.0, -0.04726], 
               [1.12465, -1.12465, -0.04726], [0.0, -1.68698, -0.04726], [-1.12465, -1.12465, -0.04726], 
               [-1.68698, 0.0, -0.04726], [-1.12465, 1.28835, -0.04726], [-9e-05, 1.36487, -0.04797]
               ]
BASE_CAM_NAME = "Camera_World_CTRL"

def make_camera_rig():
    #Start a count to check if a camera rig already exists.
    camCount = 0
    camName = BASE_CAM_NAME
    camCheck = mc.objExists(camName)

    while camCheck == True:
        camCount += 1
        camName = BASE_CAM_NAME + str(camCount)
        camCheck = mc.objExists(camName)
        if camCount > 10:
            break
    #Remove 0 from the names if no camera rigs already exist.
    if camCount == 0:
        camCount = ""

    #Make the controls. Enable their colour overrides and set their colours. Set them to hide during playback.
    worldCtrl = mc.circle(name="Camera_World_CTRL"+str(camCount), radius=12, normalY=1, normalZ=0, degree=1)[0]
    mc.setAttr(f"{worldCtrl}Shape.overrideEnabled", 1)
    mc.setAttr(f"{worldCtrl}Shape.hideOnPlayback", 1)
    mc.setAttr(f"{worldCtrl}Shape.overrideColor", 9)

    mainCtrl = mc.circle(name="Camera_Main_CTRL"+str(camCount), radius=10, normalY=1, normalZ=0, degree=3, sections=8)[0]
    #Move the control points in the circle.
    for vert in range(8):
        mc.xform(f"{mainCtrl}.cp{[vert]}", ws=True, translation=CAM_CTRL_PNTS[vert])
    mc.setAttr(f"{mainCtrl}Shape.overrideEnabled", 1)
    mc.setAttr(f"{mainCtrl}Shape.hideOnPlayback", 1)
    mc.setAttr(f"{mainCtrl}Shape.overrideColor", 14)
    mc.addAttr(mainCtrl, attributeType="bool", longName="Aim_Visibility", keyable=True, defaultValue=True)
    mc.parent(mainCtrl, worldCtrl)

    aimCtrl = mc.curve(name="Camera_Aim_CTRL"+str(camCount), point=AIM_CTRL_PNTS, ws=True)
    aimShape = mc.listRelatives(aimCtrl, shapes=True)
    mc.rename(aimShape, "Camera_Aim_CTRL"+str(camCount)+"Shape")
    mc.closeCurve(aimCtrl, replaceOriginal=True, preserveShape=0)
    mc.setAttr(f"{aimCtrl}Shape.overrideEnabled", 1)
    mc.setAttr(f"{aimCtrl}Shape.hideOnPlayback", 1)
    mc.setAttr(f"{aimCtrl}Shape.overrideColor", 22)
    mc.parent(aimCtrl, mainCtrl)

    targetCtrl = mc.curve(name="Camera_Target_CTRL"+str(camCount), point=TARGET_PNTS, ws=True)
    targetShape = mc.listRelatives(targetCtrl, shapes=True)
    mc.rename(targetShape, "Camera_Target_CTRL"+str(camCount)+"Shape")
    mc.setAttr(f"{targetCtrl}Shape.overrideEnabled", 1)
    mc.setAttr(f"{targetCtrl}Shape.hideOnPlayback", 1)
    mc.setAttr(f"{targetCtrl}Shape.overrideColor", 22)
    mc.parent(targetCtrl, mainCtrl)
    mc.xform(targetCtrl, t=(0,0,-10))
    mc.makeIdentity(targetCtrl, apply=True)

    #Aim constrain the aimCtrl to the targetCtrl.
    mc.aimConstraint(targetCtrl, aimCtrl, aimVector=(0, 0, -1), name="Camera_Aim_Constraint", worldUpType="objectRotation", worldUpObject=targetCtrl)

    #Make the camera.
    camera = mc.camera(name="Camera")[0]
    camera = mc.rename(camera, "Render_CAM"+str(camCount))
    mc.scale(5, 5, 5, camera)
    mc.parent(camera, aimCtrl)

    #Lock the camera's attributes.
    camAttrs = mc.listAttr(camera, keyable=True)
    for attr in camAttrs:
        mc.setAttr(camera+f".{attr}", lock=True, keyable=False, channelBox=False)

    #Lock unneeded attributes on controls.
    lockedCtrls = [mainCtrl, aimCtrl, targetCtrl]
    offAttrs = [".scaleX", ".scaleY", ".scaleZ", ".visibility"]
    for ctrl in lockedCtrls:
        for scale in offAttrs:
            mc.setAttr(ctrl+scale, lock=True, keyable=False, channelBox=False)
    #mc.setAttr(f"{mainCtrl}.visibility", lock=True, keyable=False, channelBox=False)

    rotAttrs = [".rotateX", ".rotateY", ".rotateZ"]
    for attr in rotAttrs:
        mc.setAttr(aimCtrl+attr, lock=True, keyable=False, channelBox=False)
    
    aimCtrls = [aimCtrl, targetCtrl]
    for ctrl in aimCtrls:
        mc.setAttr(f"{ctrl}Shape.visibility", lock=False)
        mc.connectAttr(f"{mainCtrl}.Aim_Visibility", f"{ctrl}Shape.visibility")

    mc.select(clear=True)


