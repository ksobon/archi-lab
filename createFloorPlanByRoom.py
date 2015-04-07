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

import System
from System import Array
from System.Collections.Generic import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

rooms = UnwrapElement(IN[0])
namePrefix = IN[1]
bboxOffset = IN[2]
runMe = IN[3]

def OffsetBBox(bbox, offset):
	bboxMinX = bbox.Min.X - offset
	bboxMinY = bbox.Min.Y - offset
	bboxMinZ = bbox.Min.Z - offset
	bboxMaxX = bbox.Max.X + offset
	bboxMaxY = bbox.Max.Y + offset
	bboxMaxZ = bbox.Max.Z + offset
	newBbox = BoundingBoxXYZ()
	newBbox.Min = XYZ(bboxMinX, bboxMinY, bboxMinZ)
	newBbox.Max = XYZ(bboxMaxX, bboxMaxY, bboxMaxZ)
	return newBbox

if runMe:
	viewTypes = FilteredElementCollector(doc).OfClass(ViewFamilyType)
	for i in viewTypes:
		if i.ViewFamily == ViewFamily.FloorPlan:
			viewTypeId = i.Id
			break
		else:
			continue
	
	existingPlans = FilteredElementCollector(doc).OfClass(View).ToElements()
	
	existingPlanNames, existingPlanElements = [], []
	for i in existingPlans:
		if not i.IsTemplate:
			if i.ViewType == ViewType.FloorPlan:
				existingPlanNames.append(i.ToDSType(True).Name)
				existingPlanElements.append(i)
				
	# Start Transaction
	doc = DocumentManager.Instance.CurrentDBDocument
	TransactionManager.Instance.EnsureInTransaction(doc)
	
	floorPlans = []
	for i in rooms:
		levelId = i.LevelId
		bbox = i.BoundingBox[doc.ActiveView]
		newBbox = OffsetBBox(bbox, bboxOffset)
		viewName = namePrefix + "-" + i.get_Parameter("Number").AsString() + "-" + i.get_Parameter("Name").AsString()
		if viewName in existingPlanNames:
			view = existingPlanElements[existingPlanNames.index(viewName)]
			view.CropBox = newBbox
			view.CropBoxActive = True
			view.CropBoxVisible = False
			floorPlans.append(view)
		else:
			newView = ViewPlan.Create(doc, viewTypeId, levelId)
			newView.ViewName = viewName
			newView.CropBox = newBbox
			newView.CropBoxActive = True
			view.CropBoxVisible = False
			floorPlans.append(newView)

	# End Transaction
	TransactionManager.Instance.TransactionTaskDone()
else:
	floorPlans = "Run Me set to False"
#Assign your output to the OUT variable
OUT = floorPlans
