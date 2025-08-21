import maya.cmds as mc


#Point values for custom control shapes.
CAM_CTRL_PNTS = [[0.13385, 0.0, -10.18033], [-0.78016, 0.0, -9.22674], [-7.98651, 0.0, 0.17249], [-5.59785, 0.0, 7.85356], [0.16887, 0.0, 10.24221], [5.74337, 0.0, 7.93318], [8.71342, 0.0, 0.55654], [0.86941, 0.0, -9.55085], [0.86941, 0.0, -9.55085], [0.86941, 0.0, -9.55085], [0.86941, 0.0, -9.55085]]
AIM_CTRL_PNTS = [[0.00012, 1.36504, -0.04559], [0.0, 1.28835, -1.17191], [0.0, 0.0, -1.73424], [0.0, -1.12465, -1.17191], [0.0, -1.68698, -0.04726], [0.0, -1.12465, 1.07739], [0.0, 0.0, 1.63972], [0.0, 1.28835, 1.07739], [-0.0012, 1.36509, -0.04661], [0.0012, 1.36505, -0.04893], [1.12769, 1.28227, -0.04726], [1.68698, 0.0, -0.04726], [1.12465, -1.12465, -0.04726], [0.0, -1.68698, -0.04726], [-1.12465, -1.12465, -0.04726], [-1.68698, 0.0, -0.04726], [-1.12465, 1.28835, -0.04726], [-9e-05, 1.36487, -0.04797]]
BASE_CAM_NAME = "Camera_World_CTRL"

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
worldCtrl = mc.circle(name="Camera_World_CTRL"+str(camCount), radius=15, normalY=1, normalZ=0, degree=1)[0]
mc.setAttr(f"{worldCtrl}Shape.overrideEnabled", 1)
mc.setAttr(f"{worldCtrl}Shape.hideOnPlayback", 1)
mc.setAttr(f"{worldCtrl}Shape.overrideColor", 9)

mainCtrl = mc.circle(name="Camera_Main_CTRL"+str(camCount), radius=10, normalY=1, normalZ=0)[0]
mc.setAttr(f"{mainCtrl}Shape.overrideEnabled", 1)
mc.setAttr(f"{mainCtrl}Shape.hideOnPlayback", 1)
mc.setAttr(f"{mainCtrl}Shape.overrideColor", 14)
mc.parent(mainCtrl, worldCtrl)

aimCtrl = mc.curve(name="Camera_Aim_CTRL"+str(camCount), point=CAM_CTRL_PNTS)
aimShape = mc.listRelatives(aimCtrl, shapes=True)
mc.rename(aimShape, "Camera_Aim_CTRL"+str(camCount)+"Shape")
mc.closeCurve(aimCtrl, replaceOriginal=True, preserveShape=2, blendKnotInsertion=True)
mc.setAttr(f"{aimCtrl}Shape.overrideEnabled", 1)
mc.setAttr(f"{aimCtrl}Shape.hideOnPlayback", 1)
mc.setAttr(f"{aimCtrl}Shape.overrideColor", 22)
mc.parent(aimCtrl, mainCtrl)

targetCtrl = mc.curve(name="Camera_Target_CTRL"+str(camCount), point=AIM_CTRL_PNTS)
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

#Lock unneeded attributes on other controls.
lockedCtrls = [mainCtrl, aimCtrl, targetCtrl]
offAttrs = [".scaleX", ".scaleY", ".scaleZ", ".visibility"]
for ctrl in lockedCtrls:
    for scale in offAttrs:
        mc.setAttr(ctrl+scale, lock=True, keyable=False, channelBox=False)

rotAttrs = [".rotateX", ".rotateY", ".rotateZ"]
for attr in rotAttrs:
    mc.setAttr(aimCtrl+attr, lock=True, keyable=False, channelBox=False)
