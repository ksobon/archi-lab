# Copyright(c) 2015, Konrad K Sobon
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

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

import System
from System import Array
from System.Collections.Generic import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
dsObjects = IN[0]
_symbol = UnwrapElement(IN[1])
_level = UnwrapElement(IN[2])

def toRvtPoint(point):
	unitsFactor = 3.28084 #Revit works in Feet while Dynamo in Meters
	x = point.X * unitsFactor
	y = point.Y * unitsFactor
	z = point.Z * unitsFactor
	return XYZ(x,y,z)

def toRvtType(dsObject):
	if type(dsObject) == NurbsCurve:
		points = dsObject.ControlPoints()
		rvtPoints = List[XYZ]()
		for i in points:
			rvtPoints.Add(toRvtPoint(i))
		weights = dsObject.Weights()
		rvtWeights = List[float](weights)
		knots = dsObject.Knots()
		rvtKnots = List[float](knots)
		degree = int(dsObject.Degree)
		cClosed = dsObject.IsClosed
		rational = dsObject.IsRational
		return Autodesk.Revit.DB.NurbSpline.Create(rvtPoints, rvtWeights, rvtKnots, degree, cClosed, rational)
	elif type(dsObject) == Arc:
		#convert DS Arc to Revit Arc
		startPt = toRvtPoint(dsObject.StartPoint)
		endPt = toRvtPoint(dsObject.EndPoint)
		midPt = toRvtPoint(dsObject.PointAtParameter(0.5))
		return Autodesk.Revit.DB.Arc.Create(startPt, endPt, midPt)
	elif type(dsObject) == Line:
		#convert DS Line to Revit Line
		startPt = toRvtPoint(dsObject.StartPoint)
		endPt = toRvtPoint(dsObject.EndPoint)
		return Autodesk.Revit.DB.Line.CreateBound(startPt, endPt)
	elif type(dsObject) == Circle:
		#convert DS Circle to Revit Arc (for arcs with 2pi range will be automatically converted to circle)
		center = toRvtPoint(dsObject.CenterPoint)
		radius = dsObject.Radius * 3.28084 #converted to FT from M
		startAngle = 0
		endAngle = 2 * math.pi
		xAxis = XYZ(1,0,0) #has to be normalized
		yAxis = XYZ(0,1,0) #has to be normalized
		return Autodesk.Revit.DB.Arc.Create(center, radius, startAngle, endAngle, xAxis, yAxis)
	elif type(dsObject) == NurbsCurve and dsObject.Degree < 3:
		points = []
		subCurves = dsObject.DivideEqually(26)
		for i in subCurves:
			points.append(i.StartPoint)
		points.insert(len(points), subCurves[(len(subCurves)-1)].EndPoint)
		controlPoints = List[XYZ]()
		for i in points:
			controlPoints.Add(toRvtPoint(i))
		tangents = Autodesk.Revit.DB.HermiteSplineTangents()
		endTangent = toRvtPoint(dsObject.TangentAtParameter(1))
		startTangent = toRvtPoint(dsObject.TangentAtParameter(0))
		tangents.EndTangent = endTangent.Normalize()
		tangents.StartTangent = startTangent.Normalize()
		return Autodesk.Revit.DB.HermiteSpline.Create(controlPoints, False, tangents)
	elif type(dsObject) == PolyCurve:
		subCurves = dsObject.Curves()
		points = []
		for i in subCurves:
			points.append(i.PointAtParameter(0))
			points.append(i.PointAtParameter(1))
		points = Autodesk.DesignScript.Geometry.Point.PruneDuplicates(points,0.01)
		points = process_list(toRvtPoint, points)
		rvtPoints = List[XYZ](points)
		return Autodesk.Revit.DB.PolyLine.Create(rvtPoints)	
	else:
		return dsObject.ToRevitType()

def process_list(_func, _list):
	return map( lambda x: process_list(_func, x) if type(x)==list else _func(x), _list )

try:
	errorReport = None
	#"Start" the transaction
	TransactionManager.Instance.EnsureInTransaction(doc)
	
	rvtLines = process_list(toRvtType, dsObjects)
	
	elementsOut = []
	for i in rvtLines:
		instance = doc.Create.NewFamilyInstance(i, _symbol, _level, StructuralType.Beam)
		elementsOut.append(instance)
	
	# "End" the transaction
	TransactionManager.Instance.TransactionTaskDone()
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = elementsOut
else:
	OUT = errorReport
