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

colors = IN[0]

#design script color to RVT color function
def dsColorToRvtColor(dsColor):
	R = dsColor.Red
	G = dsColor.Green
	B = dsColor.Blue
	return Autodesk.Revit.DB.Color(R,G,B)

#define color settings
colorSettings = AnalysisDisplayColorSettings()
if len(colors) == 2:
	colorSettings.MinColor = dsColorToRvtColor(colors[1])
	colorSettings.MaxColor = dsColorToRvtColor(colors[0])
elif len(colors) > 2:
	colorSettings.MaxColor = dsColorToRvtColor(colors[len(colors)-1])
	colorSettings.MinColor = dsColorToRvtColor(colors[0])
	colorList = List[AnalysisDisplayColorEntry]()
	for i in range(1, len(colors)-1, 1):
		tempColor = AnalysisDisplayColorEntry(dsColorToRvtColor(colors[i]))
		colorList.Add(tempColor)
	if colorSettings.AreIntermediateColorsValid(colorList):
		colorSettings.SetIntermediateColors(colorList)

#Assign your output to the OUT variable
OUT = colorSettings
