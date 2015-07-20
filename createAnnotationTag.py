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

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

locationPts = UnwrapElement(IN[0])
tagType = UnwrapElement(IN[1])
elements = UnwrapElement(IN[2])
RunIt = IN[4]

if isinstance(IN[3], list):
	views = [UnwrapElement(i) for i in IN[3]]
else:
	views = UnwrapElement(IN[3])

def toRvtPoint(point):
	return point.ToXyz()

def toRvtId(_id):
	if isinstance(_id, int) or isinstance(_id, str):
		id = ElementId(int(_id))
		return id
	elif isinstance(_id, ElementId):
		return _id

def ProcessList(_func, _list):
	return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

tagTypeId = toRvtId(tagType.Id)

try:
	errorReport = None
	if RunIt:
		if tagType.Category.Name == "Room Tags":
			TransactionManager.Instance.EnsureInTransaction(doc)
			roomTags = []
			if isinstance(views, list):
				for i, j, k in zip(elements, views, locationPts):
					roomId = LinkElementId(i.Id)
					location = Autodesk.Revit.DB.UV(toRvtPoint(k).X, toRvtPoint(k).Y)
					roomTag = doc.Create.NewRoomTag(roomId, location, j.Id)
					roomTag.RoomTagType = tagType
					roomTags.append(roomTag)
			else:
				for i, j in zip(elements, locationPts):
					roomId = LinkElementId(i.Id)
					location = Autodesk.Revit.DB.UV(toRvtPoint(j).X, toRvtPoint(j).Y)
					roomTag = doc.Create.NewRoomTag(roomId, location, views.Id)
					roomTag.RoomTagType = tagType
					roomTags.append(roomTag)
			TransactionManager.Instance.TransactionTaskDone()
			result = roomTags
		else:
			TransactionManager.Instance.EnsureInTransaction(doc)
			tags = []
			if isinstance(views, list):
				for i,j,k in zip(elements, views, locationPts):
					location = toRvtPoint(k)
					tag = doc.Create.NewTag(j, i, False, TagMode.TM_ADDBY_CATEGORY, TagOrientation.Horizontal, location)
					tag.ChangeTypeId(tagTypeId)
					tags.append(tag)
			else:
				for i, j in zip(elements, locationPts):
					location = toRvtPoint(j)
					tag = doc.Create.NewTag(views, i, False, TagMode.TM_ADDBY_CATEGORY, TagOrientation.Horizontal, location)
					tag.ChangeTypeId(tagTypeId)
					tags.append(tag)
			TransactionManager.Instance.TransactionTaskDone()
			result = tags
	else:
		result = "RunIt is set to False."
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = result
else:
	OUT = errorReport
