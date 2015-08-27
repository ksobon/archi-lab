# Copyright(c) 2014, Konrad K Sobon
# Grimshaw Architects, http://grimshaw-architects.com/
# Archi-lab, http://wwww.archi-lab.net

# Default imports
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc =  DocumentManager.Instance.CurrentDBDocument
app =  DocumentManager.Instance.CurrentUIApplication.Application

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#Import Collections
from System.Collections.Generic import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

levelInput = IN[0]
filterToggle = IN[1]

try:
	errorReport = None
	roomNames, validRooms = [], []
	
	collector = FilteredElementCollector(doc)
	levelFilter = ElementLevelFilter(UnwrapElement(levelInput).Id)
	
	areaFilter = AreaFilter()
	areaExcludes = collector.WherePasses(areaFilter).ToElements()
	areaExcludes = list(areaExcludes)
	
	element_set = ElementSet()
	excludes = List[ElementId]()
	if len(areaExcludes) == 0:
		logicalFilter = levelFilter
	else:
		for i in areaExcludes:
			element_set.Insert(i)
			elemIter = element_set.ForwardIterator()
			elemIter.Reset()
			while elemIter.MoveNext():
				curElem = elemIter.Current
				excludes.Add(curElem.Id)
		filter = ExclusionFilter(excludes)
		logicalFilter = LogicalAndFilter(levelFilter, filter)
	
	bip = BuiltInParameter.ROOM_NAME
	if filterToggle == False:
		allRoomsOnLevel = FilteredElementCollector(doc).OfClass(Autodesk.Revit.DB.SpatialElement).WherePasses(logicalFilter).ToElements()
		for i in allRoomsOnLevel:
			roomNames.append(i.get_Parameter(bip).AsString())
		output = allRoomsOnLevel, roomNames
	else:
		allRoomsOnLevel = FilteredElementCollector(doc).OfClass(Autodesk.Revit.DB.SpatialElement).WherePasses(logicalFilter).ToElements()
		for i in allRoomsOnLevel:
			if i.Area != 0:
				validRooms.append(i)
		for i in validRooms:
			roomNames.append(i.get_Parameter(bip).AsString())
		output = validRooms, roomNames
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = output
else:
	OUT = errorReport
