#Copyright(c) 2015, Konrad Sobon
#@arch_laboratory, http://archi-lab.net

import clr
# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
 
# Start Transaction
doc = DocumentManager.Instance.CurrentDBDocument

filter_1 = IN[1]
fam_inst = IN[0]

elements = []
for i in IN[0]:
	elements.append(UnwrapElement(i))

def TryGetToRoom(room, phase):
	try:
		toRoom = room.get_ToRoom(phase)
	except:
		toRoom = None
		pass
	return toRoom

def TryGetFromRoom(room, phase):
	try:
		fromRoom = room.get_FromRoom(phase)
	except:
		fromRoom = None
		pass
	return fromRoom

room_number, room_name, doors, room = [], [], [], []
for i in elements:
	for phase in doc.Phases:
		if i.CreatedPhaseId == phase.Id:
			for phase2 in doc.Phases:
				if TryGetToRoom(i, phase2) != None:
					to_room = TryGetToRoom(i, phase2)
					break
				else:
					to_room = None
			for phase3 in doc.Phases:
				if TryGetFromRoom(i, phase3) != None:
					from_room = TryGetFromRoom(i, phase3)
					break
				else:
					from_room = None
			filter = 0
			for f in filter_1:
				if to_room == None or f == to_room.get_Parameter("Name").AsString():
					filter += 1
			if filter > 0:
				if from_room == None and to_room == None:
					room_number.append("No to or from room")
					room_name.append("No to or from room")
					doors.append("No to or from room")
				elif from_room == None:
					room_number.append(to_room.get_Parameter("Number").AsString())
					room_name.append(to_room.get_Parameter("Name").AsString())
					doors.append(i)
					room.append(to_room)
				else:
					room_number.append(from_room.get_Parameter("Number").AsString())
					room_name.append(from_room.get_Parameter("Name").AsString())
					doors.append(i)
					room.append(from_room)
			else:
				room_number.append(to_room.get_Parameter("Number").AsString())
				room_name.append(to_room.get_Parameter("Name").AsString())
				doors.append(i)
				room.append(to_room)
					
#Assign your output to the OUT variable
OUT = room_number, room_name, doors, room
