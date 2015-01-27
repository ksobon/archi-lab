#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

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

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

_keySchedule = UnwrapElement(IN[0])
_titleTextTypeId = IN[1]
_headerTextTypeId = IN[2]
_bodyTextTypeId = IN[3]

def toRvtId(_id):
	if isinstance(_id, int) or isinstance(_id, str):
		id = ElementId(int(_id))
		return id
	elif isinstance(_id, ElementId):
		return _id

#"Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

if _titleTextTypeId != None:
	_keySchedule.TitleTextTypeId = toRvtId(_titleTextTypeId)
if _headerTextTypeId != None:
	_keySchedule.HeaderTextTypeId = toRvtId(_headerTextTypeId)
if _bodyTextTypeId != None:
	_keySchedule.BodyTextTypeId = toRvtId(_bodyTextTypeId)

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
OUT = 0
