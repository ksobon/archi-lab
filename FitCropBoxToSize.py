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

views = UnwrapElement(IN[0])
targetSize = IN[1]
runMe = IN[2]

def ViewBboxSize(view):
	scale = view.Scale
	viewBbox = view.CropBox
	viewBboxX = (viewBbox.Max.X - viewBbox.Min.X) / scale
	viewBboxY = (viewBbox.Max.Y - viewBbox.Min.Y) / scale
	return [viewBboxX, viewBboxY]
	
if runMe:			
	# Start Transaction
	TransactionManager.Instance.EnsureInTransaction(doc)
	
	floorPlans = []
	for view in views:
		if ViewBboxSize(view)[0] > targetSize[0] or ViewBboxSize(view)[1] > targetSize[1]:
			scale = view.Scale
			bbox = view.CropBox
			centerXYZ = (bbox.Max + bbox.Min) / 2.0
			if ViewBboxSize(view)[0] > targetSize[0]:
				#resize X only
				currentWidth = (bbox.Max.X - bbox.Min.X)
				targetWidth = targetSize[0] * scale
				#differenceWidth = (currentWidth - targetWidth) / 2
				newMinX = centerXYZ.X - targetWidth / 2
				newMaxX = centerXYZ.X + targetWidth / 2
			else:
				newMinX = bbox.Min.X
				newMaxX = bbox.Max.X
			if ViewBboxSize(view)[1] > targetSize[1]:
				#resize Y only
				currentHeight = (bbox.Max.Y - bbox.Min.Y)
				targetHeight = targetSize[1] * scale
				differenceHeight = (currentHeight - targetHeight) / 2
				newMinY = centerXYZ.Y - targetHeight / 2
				newMaxY = centerXYZ.Y + targetHeight / 2
			else:
				newMinY = bbox.Min.Y
				newMaxY = bbox.Max.Y
			newBbox = BoundingBoxXYZ()
			newBbox.Min = XYZ(newMinX, newMinY, bbox.Min.Z)
			newBbox.Max = XYZ(newMaxX, newMaxY, bbox.Max.Z)
			view.CropBox = newBbox
			view.CropBoxVisible = False
		floorPlans.append(view)

	# End Transaction
	TransactionManager.Instance.TransactionTaskDone()
else:
	floorPlans = "Run Me set to False"
#Assign your output to the OUT variable
OUT = floorPlans
