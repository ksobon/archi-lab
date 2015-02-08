#Copyright(c) 2014, Konrad Sobon
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
from Autodesk.Revit.DB.BuiltInCategory import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

styleName = IN[0]

modelLines = []
collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines)
paramIndex = Autodesk.Revit.DB.BuiltInParameter.BUILDING_CURVE_GSTYLE

for i in collector:
	if i.Name == "Model Lines" and i.LineStyle.Name == styleName:
		modelLines.append(i)

#Assign your output to the OUT variable
OUT = modelLines
