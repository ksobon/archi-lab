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

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

views = UnwrapElement(IN[0])
filePath = IN[1]
exportRange = System.Enum.Parse(Autodesk.Revit.DB.ExportRange, IN[2])
fileType = System.Enum.Parse(Autodesk.Revit.DB.ImageFileType, IN[3])
zoomType = System.Enum.Parse(Autodesk.Revit.DB.ZoomFitType, IN[4])
pixelSize = IN[5]
imageRes = System.Enum.Parse(Autodesk.Revit.DB.ImageResolution, IN[6])
zoom = IN[7]
fitDirection = System.Enum.Parse(Autodesk.Revit.DB.FitDirectionType, IN[8])
RunIt = IN[9]

def CreateViewSet(views):
	viewSet = List[ElementId]()
	for i in views:
		viewSet.Add(i.Id)
	return viewSet

if RunIt:
	try:
		errorReport = None
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
		
		TransactionManager.Instance.EnsureInTransaction(doc)
		doc.ExportImage(ieo)
		TransactionManager.Instance.TransactionTaskDone()
	except:
		# if error accurs anywhere in the process catch it
		import traceback
		errorReport = traceback.format_exc()
else:
	errorReport = "RunIt is set to False."

#Assign your output to the OUT variable
if errorReport == None:
	OUT = views
else:
	OUT = errorReport
