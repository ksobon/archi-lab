#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

elements = UnwrapElement(IN[0])
columnCurve = []
for i in elements:
	if i.StructuralType == StructuralType.Column:
		modelColumn = i.GetAnalyticalModel()
		if modelColumn.IsSingleCurve():
			columnCurve.append(modelColumn.GetCurve().ToProtoType())
			

#Assign your output to the OUT variable
OUT = columnCurve
