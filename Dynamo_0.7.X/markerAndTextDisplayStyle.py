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

points = IN[0]
values = IN[1]
colorSettings = IN[2]
legendSettings = IN[3]
markerSettings = IN[4]

displayStyleName = IN[5]
analysisResultName = IN[6]
analysisResultDescription = IN[7]
unitNames = IN[8]
unitMultipliers = IN[9]
displayUnit = IN[10]

message = ""

def dsPointToRvtPoint(dsPoint):
	factor = 3.2808398950
	x = dsPoint.X * factor
	y = dsPoint.Y * factor
	z = dsPoint.Z * factor
	return Autodesk.Revit.DB.XYZ(x,y,z)

def chunks(data, n):
	if n < 1:
		n = 1
	return [data[i:i + n] for i in range(0, len(data), n)]

#"Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

#create spatial field manager if one doesnt already exist
sfm = SpatialFieldManager.GetSpatialFieldManager(doc.ActiveView)
if sfm == None:
	sfm = SpatialFieldManager.CreateSpatialFieldManager(doc.ActiveView, 1)
sfm.Clear()

#get result schema index if existing else crete one
regResults = sfm.GetRegisteredResults()
if len(regResults) != 0:
	for i in regResults:
		if sfm.GetResultSchema(i).Name == analysisResultName:
			resultSchema = sfm.GetResultSchema(i)
else:
	resultSchema = AnalysisResultSchema(analysisResultName, analysisResultDescription)

names = List[str]()
multipliers = List[float]()
for i,j in zip(unitMultipliers, unitNames):
	multipliers.Add(i)
	names.Add(j)
resultSchema.SetUnits(names, multipliers)

for i in range(0, resultSchema.GetNumberOfUnits(), 1):
	if resultSchema.GetUnitsName(i) == displayUnit:
		resultSchema.CurrentUnits = i
		message = "Success! Remember that your current \ndisplay units are set to " + displayUnit
	else:
		continue
if resultSchema.GetUnitsName(resultSchema.CurrentUnits) != displayUnit:
	message = "Display Units supplied not available. \nEither add those units to results or \nspecify one of the already supplied."

schemaIndex = sfm.RegisterResult(resultSchema)

#create spatial field primitives and assign values to points
points = chunks(points, 999)
values = chunks(values, 999)
for i, j in zip(points, values):
	fieldPoints = List[Autodesk.Revit.DB.XYZ]()
	for point in i:
		fieldPoints.Add(dsPointToRvtPoint(point))
	pnts = FieldDomainPointsByXYZ(fieldPoints)
	fieldPoints.Clear()
	valList = List[ValueAtPoint]()
	doubleList = List[float]()
	for value in j:
		doubleList.Add(float(value))
		valList.Add(ValueAtPoint(doubleList))
		doubleList.Clear()
	vals = FieldValues(valList)
	valList.Clear()
	idx = sfm.AddSpatialFieldPrimitive()
	sfm.UpdateSpatialFieldPrimitive(idx, pnts, vals, schemaIndex)

#define analysis display style and set legend/color settings
collector = FilteredElementCollector(doc)
collection = collector.OfClass(AnalysisDisplayStyle).ToElements()
displayStyle = []
for i in collection:
	if i.Name == displayStyleName and i.HasMarkersAndTextSettings():
		displayStyle.append(i)
	elif i.Name == displayStyleName and not i.HasMarkersAndTextSettings():
		message = "Specified Display Style name already \nexists; please supply different name"
	else:
		continue
if len(displayStyle) == 0:
	try:
		analysisDisplayStyle = AnalysisDisplayStyle.CreateAnalysisDisplayStyle(doc, displayStyleName, markerSettings, colorSettings, legendSettings)
	except:
		pass
else:
	analysisDisplayStyle = displayStyle[0]
	analysisDisplayStyle.SetLegendSettings(legendSettings)
	analysisDisplayStyle.SetColorSettings(colorSettings)
	analysisDisplayStyle.SetMarkersAndTextSettings(markerSettings)

try:
	doc.ActiveView.AnalysisDisplayStyleId = analysisDisplayStyle.Id
except:
	pass

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
if len(message) != 0:
	OUT = '\n'.join('{:^35}'.format(s) for s in message.split('\n'))
else:
	OUT = 0
