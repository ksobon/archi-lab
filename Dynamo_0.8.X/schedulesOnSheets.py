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

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

elements = []
for i in IN[0]:
	elements.append(UnwrapElement(i))

try:
	errorReport = None
	# "Start" the transaction
	trans = Transaction(doc, "Temp Transaction")
	trans.Start()
	
	schName, schId, ids = [], [], []
	for i in elements:
		ids.append(doc.Delete(i.Id))
	trans.RollBack()
	
	elementsOnSheet = []
	for i in ids:
		for id in i:
			if doc.GetElement(id) != None:
				elementsOnSheet.append(doc.GetElement(id))
				
	schedules = []
	for i in elementsOnSheet:
		try:
			schedules.append(doc.GetElement(i.ScheduleId))
		except:
			pass
			
	uniqueSchedules = set()
	for i in schedules:
		if i.Id.ToString() not in uniqueSchedules:
			uniqueSchedules.add(i.Id.ToString())
			
	schedulesSheet = []
	for i in uniqueSchedules:
		idInt = int(i)
		elemId = ElementId(idInt)
		schedulesSheet.append(doc.GetElement(elemId).ToDSType(True))
	
	viewSchedules = FilteredElementCollector(doc).OfClass(ViewSchedule).ToElements()
	
	notOnSheet = set()
	for i in viewSchedules:
		if i.Id.ToString() in uniqueSchedules:
			continue
		else:
			notOnSheet.add(i.Id.ToString())
	
	schedulesNotSheet = []
	for i in notOnSheet:	
		idInt = int(i)
		elemId = ElementId(idInt)
		schedulesNotSheet.append(doc.GetElement(elemId).ToDSType(True))
		
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = schedulesSheet, schedulesNotSheet
else:
	OUT = errorReport
