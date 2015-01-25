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

markerType = IN[0]
markerSize = IN[1]
TextTypeId = IN[2]
rounding = IN[3]
textLabelType = IN[4]

#define marker settings
markerSettings = AnalysisDisplayMarkersAndTextSettings()

#marker
if markerType == "Circle":
	markerSettings.MarkerType = AnalysisDisplayStyleMarkerType.Circle
elif markerType == "Square":
	markerSettings.MarkerType = AnalysisDisplayStyleMarkerType.Square
elif markerType == "Triangle":
	markerSettings.MarkerType = AnalysisDisplayStyleMarkerType.Triangle
else:
	message = "Please specify one of the marker types: \nCircle, Square or Triangle"
markerSettings.MarkerSize = markerSize

#text annotation
if textLabelType == "ShowAll":
	markerSettings.TextLabelType = AnalysisDisplayStyleMarkerTextLabelType.ShowAll
elif textLabelType == "ShowNone":
	markerSettings.TextLabelType = AnalysisDisplayStyleMarkerTextLabelType.ShowNone
elif textLabelType == "ShowPredefined":
	markerSettings.TextLabelType = AnalysisDisplayStyleMarkerTextLabelType.ShowPredefined
else:
	message = "Please specify one of the text label types: \nShowAll, ShowNone or ShowPredefined"
markerSettings.TextTypeId = TextTypeId[0]
markerSettings.Rounding = rounding

#Assign your output to the OUT variable
OUT = markerSettings
