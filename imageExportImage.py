#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import Element wrapper extension methods
clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import RevitAPI
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

import System
from System import Array
from System.Collections.Generic import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

views = UnwrapElement(IN[0])
filePath = IN[1]
exportRange = IN[2]
fileType = IN[3]
zoomType = IN[4]
pixelSize = IN[5]
imageRes = IN[6]
zoom = IN[7]
fitDirection = IN[8]

def CreateViewSet(views):
	viewSet = List[ElementId]()
	for i in views:
		viewSet.Add(i.Id)
	return viewSet


ieo = ImageExportOptions()
ieo.FilePath = filePath

if fileType != None:
	ieo.HLRandWFViewsFileType = fileType

if zoomType != None:
	ieo.ZoomType = zoomType
	if ieo.ZoomType == ZoomFitType.FitToPage:
		if imageRes != None:
			ieo.ImageResolution = imageRes
		if pixelSize != None:
			ieo.PixelSize = pixelSize
		if fitDirection != None:
			ieo.FitDirection = fitDirection
	elif ieo.ZoomType == ZoomType.Zoom:
		if zoom != None:
			ieo.Zoom = zoom

if len(views) > 1:
	ieo.ExportRange = ExportRange.SetOfViews
	ieo.SetViewsAndSheets(CreateViewSet(views))
else:
	ieo.ExportRange = exportRange

# "Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

doc.ExportImage(ieo)

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
OUT = 0
