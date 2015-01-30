#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

from System.Collections.Generic import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

def toRvtId(_id):
	if isinstance(_id, int) or isinstance(_id, str):
		id = ElementId(int(_id))
		return id
	elif isinstance(_id, ElementId):
		return _id

lmntIds, axises, angles = [], [], []
for i, j in zip(IN[0], IN[1]):
	lmntIds.append(toRvtId(UnwrapElement(i)))
	axises.append(j.ToRevitType())
angles = IN[2]

# "Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

elements = []
for axis_, angle_, lmntId_ in zip(axises, angles, lmntIds):
	Autodesk.Revit.DB.ElementTransformUtils.RotateElement(doc, lmntId_, axis_, angle_)
	elements.append(doc.GetElement(lmntId_))

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
OUT = elements
