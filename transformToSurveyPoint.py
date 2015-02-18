#Copyright(c) 2015, Konrad Sobon
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

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

from System.Collections.Generic import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
inPoints = IN[0]

def toRvtPoint(point):
	x = Autodesk.Revit.DB.UnitUtils.Convert(point.X, DisplayUnitType.DUT_METERS, DisplayUnitType.DUT_DECIMAL_FEET)
	y = Autodesk.Revit.DB.UnitUtils.Convert(point.Y, DisplayUnitType.DUT_METERS, DisplayUnitType.DUT_DECIMAL_FEET)
	z = Autodesk.Revit.DB.UnitUtils.Convert(point.Z, DisplayUnitType.DUT_METERS, DisplayUnitType.DUT_DECIMAL_FEET)
	return Autodesk.Revit.DB.XYZ(x,y,z)

def toDynPoint(point):
	x = Autodesk.Revit.DB.UnitUtils.Convert(point.X, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_METERS)
	y = Autodesk.Revit.DB.UnitUtils.Convert(point.Y, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_METERS)
	z = Autodesk.Revit.DB.UnitUtils.Convert(point.Z, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_METERS)
	return Autodesk.DesignScript.Geometry.Point.ByCoordinates(x,y,z)

def processListArg(_func, _list, _arg):
	return map( lambda x: processListArg(_func, x, _arg) if type(x)==list else _func(x, _arg), _list )

def transformPoint(point, transform):
	rvtPt = transform.OfPoint(toRvtPoint(point))
	return toDynPoint(rvtPt)

currentLocation = doc.ActiveProjectLocation
projectPosition = currentLocation.get_ProjectPosition(XYZ.Zero)
z = projectPosition.Elevation
x = projectPosition.EastWest
y = projectPosition.NorthSouth
transform = Transform.CreateTranslation(XYZ(x,y,z))

#Assign your output to the OUT variable
if type(inPoints) == list:
	OUT = processListArg(transformPoint, inPoints, transform)
else:
	OUT = transformPoint(inPoints, transform)
