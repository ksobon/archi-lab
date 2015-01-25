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

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Analysis import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

showLegend = IN[0]
showUnits = IN[1]
showName = IN[2]
headingTextTypeId = IN[3]
bodyTextTypeId = IN[4]
dataDescription = IN[5]
rounding = IN[6]
height = IN[7]
width = IN[8]
steps = IN[9]

#define legend settings
legendSettings = AnalysisDisplayLegendSettings()
if showLegend:
	legendSettings.ShowLegend = True
	#heading
	legendSettings.ShowUnits = showUnits
	legendSettings.ShowDataName = showName
	legendSettings.HeadingTextTypeId = headingTextTypeId[0]
	#body
	legendSettings.TextTypeId = bodyTextTypeId[0]
	legendSettings.ShowDataDescription = dataDescription
	legendSettings.Rounding = rounding
	#color range
	legendSettings.ColorRangeHeight = height
	legendSettings.ColorRangeWidth = width
	legendSettings.NumberOfSteps = steps
else:
	legendSettings.ShowLegend = False

#Assign your output to the OUT variable
OUT = legendSettings
