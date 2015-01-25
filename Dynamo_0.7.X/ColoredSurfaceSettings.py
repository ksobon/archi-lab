#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

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
from Autodesk.Revit.DB.Analysis import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

showGridlines = IN[0]
showContour = IN[1]
lineWeight = IN[2]
gridColor = IN[3]

#design script color to RVT color function
def dsColorToRvtColor(dsColor):
	R = dsColor.Red
	G = dsColor.Green
	B = dsColor.Blue
	return Autodesk.Revit.DB.Color(R,G,B)

#define colored surface settings
coloredSurfaceSettings = AnalysisDisplayColoredSurfaceSettings()
coloredSurfaceSettings.ShowGridLines = showGridlines
coloredSurfaceSettings.ShowContourLines = showContour
coloredSurfaceSettings.GridLineWeight = lineWeight
coloredSurfaceSettings.GridColor = dsColorToRvtColor(gridColor)

#Assign your output to the OUT variable
OUT = coloredSurfaceSettings
