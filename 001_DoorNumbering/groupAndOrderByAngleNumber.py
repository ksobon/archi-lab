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


from itertools import groupby

room_number = IN[0]
angle = IN[1]
door = IN[2]

grps = sorted(zip(room_number, angle, door), key=lambda x: (x[0], x[1]))
room_number, angle, door = [], [] ,[]
for i, grp in groupby(grps, lambda x: x[0]):
	sub_rm_number, sub_angle, sub_door = [], [] ,[]
	for j in grp:
		sub_rm_number.append(j[0])
		sub_angle.append(j[1])
		sub_door.append(j[2])
	room_number.extend(sub_rm_number)
	angle.extend(sub_angle)
	door.extend(sub_door)

OUT = room_number ,angle, door
