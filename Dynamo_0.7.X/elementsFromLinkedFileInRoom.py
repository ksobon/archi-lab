#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

# This code is based on Family.InRoom node originally created
# by Peter Kompolschek and published on Dynamo blog. Big thanks 
# to Peter for sharing his work so graciously.

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

from System.Collections.Generic import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

rvtLink = UnwrapElement(IN[2])
transform = rvtLink.GetTotalTransform()

def FamiliesInRoom(_room, _families, _transform):
	outList = []
	for family in _families:
		pt = _transform.OfPoint(family.Location.Point)
		if _room.IsPointInRoom(pt):
			outList.append(family)
	return outList

families = []
for i in IN[0]:
	families.append(UnwrapElement(i))

rooms = []
for i in IN[1]:
	if UnwrapElement(i).Area > 0:
		rooms.append(UnwrapElement(i))

outData = [[] for i in range(len(rooms))]
for index, room in enumerate(rooms):
	outData[index].extend(FamiliesInRoom(room, families, transform))

OUT = outData
