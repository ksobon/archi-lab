# Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

# Import DocumentManager and TransactionManager
import clr
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import System
from System.Collections.Generic import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import System

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
	if heading != None:
		field.ColumnHeading = heading
	if hidden != None:
		field.IsHidden = hidden
	if hOrientation != None:
		field.HeadingOrientation = System.Enum.Parse(Autodesk.Revit.DB.ScheduleHeadingOrientation, hOrientation)
	if hAlign != None:
		field.HorizontalAlignment = System.Enum.Parse(Autodesk.Revit.DB.ScheduleHorizontalAlignment, hAlign)
	if sWidth != None:
		field.SheetColumnWidth = sWidth
	return None

try:
	errorReport = None
	
	TransactionManager.Instance.EnsureInTransaction(doc)
	if type(_paramName) == list:
		for i, j, k, l, m, n in zip(_paramName, _columnHeading, _hidden, _headingOrientation, _horizontalAlignment, _sheetColumnWidth):
			scheduleField = getField(_keySchedule, i)
			message = formatColumn(scheduleField, j, k, l, m , n)
	else:
		scheduleField = getField(_keySchedule, _paramName)
		message = formatColumn(scheduleField, _columnHeading, _hidden, _headingOrientation, _horizontalAlignment, _sheetColumnWidth)
	
	TransactionManager.Instance.TransactionTaskDone()
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = 0
else:
	OUT = errorReport
