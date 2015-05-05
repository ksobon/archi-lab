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

door_x = IN[0]
room_x = IN[1]
angle = IN[2]
result = []

for i, j, k in zip(door_x, room_x, angle):
	if i <= j:
		result.append(math.pi+((math.pi)-k))
	else:
		result.append(k)

#Assign your output to the OUT variable
OUT = result
