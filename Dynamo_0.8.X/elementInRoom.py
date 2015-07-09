#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

# This code is based on Family.InRoom node originally created
# by Peter Kompolschek and published on Dynamo blog. Big thanks 
# to Peter for sharing his work so graciously.

import clr
import sys
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

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

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

def TryGetRoom(room, phase):
	try:
		inRoom = room.Room[phase]
	except:
		inRoom = None
		pass
	return inRoom

def FamiliesInRoom(_room, _families, _doc):
	outList = []
	for family in _families:
		pt = family.Location.Point
		if _room.IsPointInRoom(pt):
			outList.append(family)
		else:
			for phase in _doc.Phases:
				inRoom = TryGetRoom(family, phase)
				if inRoom != None and inRoom.ToDSType(True).Name == _room.ToDSType(True).Name:
					outList.append(family)
	return outList

try:
	errorReport = None
	families = []
	for i in IN[0]:
		families.append(UnwrapElement(i))
	
	rooms = []
	for i in IN[1]:
		if UnwrapElement(i).Area > 0:
			rooms.append(UnwrapElement(i))
	
	outData = [[] for i in range(len(rooms))]
	for index, room in enumerate(rooms):
		outData[index].extend(FamiliesInRoom(room, families, doc))
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = outData
else:
	OUT = errorReport
