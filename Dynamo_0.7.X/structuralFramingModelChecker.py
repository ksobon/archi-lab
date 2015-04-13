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

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

columns = UnwrapElement(IN[0])
framing = UnwrapElement(IN[1])

def ProcessList(_func, _list):
    return map( lambda x: process_list(_func, x) if type(x)==list else _func(x), _list )

def FindClosestPoint(pointCloud, testPoint):
	distanceList = []
	for point in pointCloud:
		distanceList.append(point.DistanceTo(testPoint))
	index = distanceList.index(min(distanceList))
	closestPoint = pointCloud[index]
	return closestPoint

def GetStructuralColumnCurve(item):
	if item.StructuralType == StructuralType.Column:
		modelColumn = item.GetAnalyticalModel()
		if modelColumn.IsSingleCurve():
			return modelColumn.GetCurve().ToProtoType()
		else:
			return None

columnCurves = ProcessList(GetStructuralColumnCurve, columns)
columnPoints = []
for i in columnCurves:
	columnPoints.append(i.PointAtParameter(0))
	columnPoints.append(i.PointAtParameter(1))

#"Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

for i in framing:
	if i.StructuralType == StructuralType.Brace:
		dsCurve = i.Location.Curve.ToProtoType()
		dsStartPoint = dsCurve.PointAtParameter(0)
		dsEndPoint = dsCurve.PointAtParameter(1)
		newStartPoint = FindClosestPoint(columnPoints, dsStartPoint)
		newEndPoint = FindClosestPoint(columnPoints, dsEndPoint)
		newCurve = Autodesk.DesignScript.Geometry.Line.ByStartPointEndPoint(newStartPoint, newEndPoint)
		newRvtCurve = newCurve.ToRevitType()
		type = i.Symbol
		bipName = BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM
		levelId = i.get_Parameter(bipName).AsElementId()
		level = doc.GetElement(levelId)
		doc.Create.NewFamilyInstance(newRvtCurve, type, level, StructuralType.Brace)
		doc.Delete(i.Id)
	else:
		dsCurve = i.Location.Curve.ToProtoType()
		dsStartPoint = dsCurve.PointAtParameter(0)
		dsEndPoint = dsCurve.PointAtParameter(1)
		newStartPoint = FindClosestPoint(columnPoints, dsStartPoint)
		newEndPoint = FindClosestPoint(columnPoints, dsEndPoint)
		newCurve = Autodesk.DesignScript.Geometry.Line.ByStartPointEndPoint(newStartPoint, newEndPoint)
		i.Location.Curve = newCurve.ToRevitType()

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
OUT = 0
