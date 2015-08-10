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

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import math
#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

dsCurves = IN[0]
wallType = IN[1]
level = IN[2]
structural = IN[3]

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def toRvtType(dsObject):
	if type(dsObject) == NurbsCurve:
		points = dsObject.ControlPoints()
		rvtPoints = List[XYZ]()
		for i in points:
			rvtPoints.Add(XYZ(i.X, i.Y, i.Z))
		weights = dsObject.Weights()
		rvtWeights = List[float](weights)
		knots = dsObject.Knots()
		rvtKnots = List[float](knots)
		degree = int(dsObject.Degree)
		cClosed = dsObject.IsClosed
		rational = dsObject.IsRational
		return Autodesk.Revit.DB.NurbSpline.Create(rvtPoints, rvtWeights, rvtKnots, degree, cClosed, rational)
	elif type(dsObject) == Circle:
		#convert DS Arc to Revit Arc
		# extract ds circle properties
		pt0 = dsObject.PointAtParameter(0)
		pt1 = dsObject.PointAtParameter(0.25)
		dsVectorY = Vector.ByTwoPoints(dsObject.CenterPoint, pt1).Normalized()
		dsVectorX = Vector.ByTwoPoints(dsObject.CenterPoint, pt0).Normalized()
		# create revit plane from x,y vectors and origin
		xVec = XYZ(dsVectorX.X, dsVectorX.Y, dsVectorX.Z)
		yVec = XYZ(dsVectorY.X, dsVectorY.Y, dsVectorY.Z)
		origin = XYZ(dsObject.CenterPoint.X, dsObject.CenterPoint.Y, dsObject.CenterPoint.Z)
		plane = Autodesk.Revit.DB.Plane(xVec, yVec, origin)
		# create revit arc from plane, radius, angles
		radius = dsObject.Radius
		startAngle = 0
		endAngle = math.pi * 2
		arc1 = Autodesk.Revit.DB.Arc.Create(plane, radius, 0, math.pi)
		arc2 = Autodesk.Revit.DB.Arc.Create(plane, radius, math.pi, endAngle)
		return [arc1, arc2]
	elif type(dsObject) == Line:
		#convert DS Line to Revit Line
		startPt = XYZ(dsObject.StartPoint.X, dsObject.StartPoint.Y, dsObject.StartPoint.Z)
		endPt = XYZ(dsObject.EndPoint.X, dsObject.EndPoint.Y, dsObject.EndPoint.Z)
		return Autodesk.Revit.DB.Line.CreateBound(startPt, endPt)
	elif type(dsObject) == Arc:
		#convert DS Arc to Revit Arc
		startPt = XYZ(dsObject.StartPoint.X, dsObject.StartPoint.Y, dsObject.StartPoint.Z)
		endPt = XYZ(dsObject.EndPoint.X, dsObject.EndPoint.Y, dsObject.EndPoint.Z)
		midPt = XYZ(dsObject.PointAtParameter(0.5).X, dsObject.PointAtParameter(0.5).Y, dsObject.PointAtParameter(0.5).Z) 
		return Autodesk.Revit.DB.Arc.Create(startPt, endPt, midPt)
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

def Flatten(*args):
    for x in args:
        if hasattr(x, '__iter__'):
            for y in Flatten(*x):
                yield y
        else:
            yield x

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

try:
	errorReport = None
	walls = []
	# check list depth
	# if list has sublists then process as such
	# check for PolyCurve class
	# if input is PolyCurve then implement conversion
	rvtCurves = Flatten(ProcessList(toRvtType, dsCurves))
	profile = List[Autodesk.Revit.DB.Curve]()
	for i in rvtCurves:
		profile.Add(i)
	wallTypeId = wallType.Id
	levelId = level.Id
	try:
		walls.append(Wall.Create(doc, profile, structural))
		#walls.append(Wall.Create(doc, profile, ElementId(wallTypeId), ElementId(levelId), structural))
	except:
		pass
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

# check if there is a way to stop Dynamo from constant re-creation
# of the element in question I dont want to create a new wall every single time.
# End Transaction
TransactionManager.Instance.TransactionTaskDone()


#Assign your output to the OUT variable
if errorReport == None:
	OUT = walls
else:
	OUT = errorReport
