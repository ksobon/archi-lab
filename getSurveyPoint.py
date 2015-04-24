#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
inPoints = IN[0]

def toDynPoint(point):
	x = Autodesk.Revit.DB.UnitUtils.Convert(point.X, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_METERS)
	y = Autodesk.Revit.DB.UnitUtils.Convert(point.Y, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_METERS)
	z = Autodesk.Revit.DB.UnitUtils.Convert(point.Z, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_METERS)
	return Autodesk.DesignScript.Geometry.Point.ByCoordinates(x,y,z)

surveyPoints = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_SharedBasePoint).ToElements()

bipEW = BuiltInParameter.BASEPOINT_EASTWEST_PARAM
bipNS = BuiltInParameter.BASEPOINT_NORTHSOUTH_PARAM
bipElev = BuiltInParameter.BASEPOINT_ELEVATION_PARAM

eastWest = surveyPoints[0].get_Parameter(bipEW).AsDouble()
northSouth = surveyPoints[0].get_Parameter(bipNS).AsDouble()
elev = surveyPoints[0].get_Parameter(bipElev).AsDouble()

OUT = toDynPoint(XYZ(eastWest, northSouth, elev))
