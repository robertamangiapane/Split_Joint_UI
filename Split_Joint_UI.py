import maya.cmds as cmds

mainWindow = None

def CreateWindow(windowName):

    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName)

    global mainWindow
    mainWindow = cmds.window(windowName, title=windowName)

    cmds.showWindow(mainWindow)
    return mainWindow


def SplitJointUI():


    editedWindow = CreateWindow("Split_Joint")
    cmds.window(editedWindow, edit=True, title="Split_Joint", widthHeight=(300, 100))
    cmds.rowColumnLayout(nc=2, cal=[(1, "center"), (2, "center")], columnWidth=[(1, 150), (2, 150)],
                         cat=[(1, "both", 10), (2, "both", 10)], rs=[(1, 10), (2, 10)],
                         rat=[(1, "both", 10), (2, "both", 5)])
    cmds.text(label="Segments")
    intSegmentsField = cmds.intField(min=2, max=100)
    cmds.button(label="Okay", c=InsertJoint)
    global intSegmentsField
    cmds.button(label="Cancel", c="cmds.intField(intSegmentsField, edit=True, v=2)")


def GetSelection():
    selection = cmds.ls(selection=True)
    if len(selection) == 0 or len(selection) > 1:
        raise Exception("You must select ONE joint")
    return selection[0]


def GetParentRadius():
    parentJoint = GetSelection()
    parentRadius = cmds.joint(parentJoint, query=True, rad=True)
    return parentRadius[0]


def GetDistance():
    startJoint = GetSelection()
    startJointChildren = cmds.listRelatives(startJoint)
    if not startJointChildren:
        raise Exception("You must select the parent joint")

    endJoint = startJointChildren[0]
    distance = cmds.getAttr(endJoint + '.translateX')
    return distance


def OrientJoint():
    startJoint = GetSelection()
    cmds.joint(startJoint, edit=True, orientJoint="xzy", secondaryAxisOrient="yup", ch=True, zso=True)


def InsertJoint(*args):
    OrientJoint()
    parentRadius = GetParentRadius()
    segments = GetFieldValue()
    mainJoint = GetSelection()
    distance = GetDistance()
    distanceSegments = distance / segments
    jointToInsert = segments - 1
    i = 1
    prevJoint = mainJoint

    while i <= jointToInsert:
        newJoint = cmds.insertJoint(prevJoint)
        cmds.joint(newJoint, edit=True, co=True, r=True, p=(distanceSegments, 0, 0), rad=(parentRadius))
        prevJoint = newJoint
        i += 1

    global mainWindow
    cmds.deleteUI(mainWindow)


def GetFieldValue():
    global intSegmentsField
    intValue = cmds.intField(intSegmentsField, query=True, v=True)
    return intValue

SplitJointUI()
