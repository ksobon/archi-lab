#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

from System.Collections.Generic import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

rooms = UnwrapElement(IN[0])
views = UnwrapElement(IN[1])
familyType = UnwrapElement(IN[2])
runMe = IN[3]

#"Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

test = []
if runMe:
	roomTags = []
	for room, view in zip(rooms, views):
		roomId = LinkElementId(room.Id)
		bbox = view.CropBox
		XYZLocation = (bbox.Max + bbox.Min) / 2.0
		location = Autodesk.Revit.DB.UV(XYZLocation.X + 0.2, XYZLocation.Y - 5.6)
		roomTag = doc.Create.NewRoomTag(roomId, location, view.Id)
		roomTag.RoomTagType = familyType
		roomTags.append(roomTag)
else:
	roomTags = "Run Me set to False"

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
OUT = roomTags
