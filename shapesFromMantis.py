#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import System
from System import Array
from System.Collections.Generic import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

def mToFt(item):
	return float(item[0]) * 3.28084

def process_list(_func, _list):
	return map( lambda x: process_list(_func, x) if type(x)==list else _func(x), _list )

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



rvtPoints = process_list(toRvtPoint, IN[0])

templateFileName = IN[2]
fdoc = app.NewFamilyDocument(templateFileName)
factory = fdoc.FamilyCreate
creaapp = fdoc.Application.Create

#"Start" the transaction
#TransactionManager.Instance.EnsureInTransaction(fdoc)

t = Transaction(fdoc, "Create New Family")
t.Start()


failOptions = t.GetFailureHandlingOptions()
failList  = t.GetFailureMessages()
#failOptions.SetFailuresPreprocessor()


plane = Plane(XYZ(1,0,0), XYZ(0,1,0), XYZ(0,0,0))
sketchPlane = SketchPlane.Create(fdoc, plane)

for pts, ht in zip(rvtPoints, IN[1]):
	curveArrArray = CurveArrArray()
	curveArray = CurveArray()
	
	for i in range(0, len(pts)-1, 1):
		modelLine = creaapp.NewLineBound(pts[0],pts[1])
		curveArray.Append(modelLine)
		pts.pop(0)
	
	curveArrArray.Append(curveArray)
	extrusionHeight = mToFt(ht)
	#extrusionForm = factory.NewExtrusion(True, curveArrArray, sketchPlane, extrusionHeight)
	#extrusionForm = doc.NewExtrusion(True, curveArrArray, sketchPlane, mToFt(ht))

t.Commit()
# "End" the transaction
#TransactionManager.Instance.TransactionTaskDone()

# Force Close the transaction
#TransactionManager.ForceCloseTransaction()

fileName = IN[3]
opt = SaveAsOptions()
opt.OverwriteExistingFile = True

fdoc.SaveAs(fileName, opt)
fdoc.Close(False)



#t.SetFailureHandlingOptions(failOpt)
#Assign your output to the OUT variable
OUT = accessor
