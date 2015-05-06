#Copyright(c) 2015, Konrad Sobon
#@arch_laboratory, http://archi-lab.net

# Default imports
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#The input to this node will be stored in the IN[0]...INX variable(s).
dataEnteringNode = IN[0]
import math

repAngle = IN[0]
roomX = IN[1]
roomY = IN[2]
doorX = IN[3]
doorY = IN[4]

result = []
for a, rx, ry, dx, dy in zip(repAngle, roomX, roomY, doorX, doorY):
	if dx >= rx  and dy >= ry:
		angle = a
	elif dx >= rx and dy <= ry:
		angle = 180 - a
	elif dx <= rx and dy <= ry:
		angle = 180 + a
	elif dx <= rx and dy >= ry:
		angle = 360 - a
	result.append(angle)

#Assign your output to the OUT variable
OUT = result
