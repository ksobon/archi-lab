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

_keySchedule = UnwrapElement(IN[0])
_paramName = IN[1]
_columnHeading = IN[2]
_hidden = IN[3]
_headingOrientation = IN[4]
_horizontalAlignment = IN[5]
_sheetColumnWidth = IN[6]

def getField(schedule, name):
	definition = schedule.Definition
	count = definition.GetFieldCount()
	for i in range(0, count, 1):
		if definition.GetField(i).GetName() == name:
			field = definition.GetField(i)
	return field

def formatColumn(field, heading, hidden, hOrientation, hAlign, sWidth):
	message = None
	if heading != None:
		field.ColumnHeading = heading
	if hidden != None:
		field.IsHidden = hidden
	if hOrientation != None:
		if hOrientation == "Horizontal":
			ho = ScheduleHeadingOrientation.Horizontal
			field.HeadingOrientation = ho
		elif hOrientation == "Vertical":
			ho = ScheduleHeadingOrientation.Vertical
			field.HeadingOrientation = ho
		else:
			message = "Schedule Heading Orientation can only \nbe set to Horizontal or Vertical. \nPlease check your spelling."
	if hAlign != None:
		if hAlign == "Left":
			ha = ScheduleHorizontalAlignment.Left
			field.HorizontalAlignment = ha
		elif hAlign == "Center":
			ha = ScheduleHorizontalAlignment.Center
			field.HorizontalAlignment = ha
		elif hAlign == "Right":
			ha = ScheduleHorizontalAlignment.Right
			field.HorizontalAlignment = ha
		else:
			message = "Schedule Horizontal Alignment can only \nbe set to Left, Center or Right. \nPlease check your spelling."
	if sWidth != None:
		field.SheetColumnWidth = sWidth
	return message

#"Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

message = None
if type(_paramName) == list:
	for i, j, k, l, m, n in zip(_paramName, _columnHeading, _hidden, _headingOrientation, _horizontalAlignment, _sheetColumnWidth):
		scheduleField = getField(_keySchedule, i)
		message = formatColumn(scheduleField, j, k, l, m , n)
else:
	scheduleField = getField(_keySchedule, _paramName)
	message = formatColumn(scheduleField, _columnHeading, _hidden, _headingOrientation, _horizontalAlignment, _sheetColumnWidth)

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
if message == None:
	OUT = 0
else:
	OUT = '\n'.join('{:^35}'.format(s) for s in message.split('\n'))
