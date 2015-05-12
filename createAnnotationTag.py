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

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

points = UnwrapElement(IN[0])
symType = UnwrapElement(IN[1])
families = UnwrapElement(IN[2])
views = UnwrapElement(IN[3])
boolean = IN[4]

def toRvtPoint(point):
	return Autodesk.Revit.DB.XYZ(point.X,point.Y,point.Z)

def toRvtId(_id):
	if isinstance(_id, int) or isinstance(_id, str):
		id = ElementId(int(_id))
		return id
	elif isinstance(_id, ElementId):
		return _id

def process_list(_func, _list):
	return map( lambda x: process_list(_func, x) if type(x)==list else _func(x), _list )

symTypeId = toRvtId(symType.Id)
rvtPoints = process_list(toRvtPoint, points)

#"Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

msg = None
if boolean:
	tags = []
	if len(views) != 1:
		for i,j,k in zip(families,rvtPoints,views):
			tag = doc.Create.NewTag(k, i, False, TagMode.TM_ADDBY_CATEGORY, TagOrientation.Horizontal, j)
			tag.ChangeTypeId(symTypeId)
			tags.append(tag)
	else:
		for i, j in zip(families, rvtPoints):
			tag = doc.Create.NewTag(views, i, False, TagMode.TM_ADDBY_CATEGORY, TagOrientation.Horizontal, j)
			tag.ChangeTypeId(symTypeId)
			tags.append(tag)
else:
	msg = "Boolean set to false"

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
if msg != None:
	OUT = msg
else:
	OUT = tags
