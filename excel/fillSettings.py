import clr
import sys
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

patternType = IN[0]
backColor = IN[1]
foreColor = IN[2]
opacity = IN[3]
bevelType = IN[4]

bcolor = ",".join([str(backColor.Red), str(backColor.Green), str(backColor.Blue)])
fcolor = ",".join([str(foreColor.Red), str(foreColor.Green), str(foreColor.Blue)])
cellFill = "~".join([patternType, bcolor, fcolor, str(opacity), bevelType])

#Assign your output to the OUT variable
OUT = cellFill
