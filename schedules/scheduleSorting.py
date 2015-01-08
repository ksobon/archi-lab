#Copyright(c) 2014, Konrad Sobon
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

keySchedule = UnwrapElement(IN[0])
paramName = IN[1]
_showBlankLine = IN[2]
_footerCount = IN[3]
_footerTitle = IN[4]
_header = IN[5]
_sortOrder = IN[6]

#"Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

message = None

definition = keySchedule.Definition
if definition.GetSortGroupFieldCount() != 0:
	definition.ClearSortGroupFields()
count = definition.GetFieldCount()

for i in range(0, count, 1):
	if definition.GetField(i).GetName() == paramName:
		fieldId = definition.GetField(i).FieldId

ssgf = ScheduleSortGroupField()
ssgf.FieldId = fieldId

if _showBlankLine != None:
	ssgf.ShowBlankLine = _showBlankLine

checkList = [_footerCount, _footerTitle]
if any(item == True for item in checkList):
	ssgf.ShowFooter = True
	if _footerCount != None:
		ssgf.ShowFooterCount = _footerCount
	if _footerTitle != None:
		ssgf.ShowFooterTitle = _footerTitle
else:
	ssgf.ShowFooter = False

if _header != None:
	ssgf.ShowHeader = _header
if _sortOrder != None:
	if _sortOrder == "Ascending":
		sOrder = ScheduleSortOrder.Ascending
		ssgf.SortOrder = sOrder
	elif _sortOrder == "Descending":
		sOrder = ScheduleSortOrder.Descending
		ssgf.SortOrder = sOrder
	else:
		message = "Schedule Sort Order can only be set to Ascending or Descending."

definition.AddSortGroupField(ssgf)

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
if message == None:
	OUT = 0
else:
	OUT = '\n'.join('{:^35}'.format(s) for s in message.split('\n'))
