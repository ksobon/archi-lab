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

values = IN[0]
surfaces = IN[1]
UVPoints = IN[2]

colorSettings = IN[3]
legendSettings = IN[4]
styleSettings = IN[5]

displayStyleName = IN[6]
analysisResultName = IN[7]
analysisResultDescription = IN[8]
unitNames = IN[9]
unitMultipliers = IN[10]
displayUnit = IN[11]

message = None

def getFace(element):
	#create geometry options/compute references
	geoOptions = Options()
	geoOptions.ComputeReferences = True
	#extract geometry
	geoElement = element.get_Geometry(geoOptions)
	geoSet = List[GeometryInstance]()
	elemIter = geoElement.GetEnumerator()
	elemIter.Reset()
	while elemIter.MoveNext():
		curElem = elemIter.Current
		geoSet.Add(curElem)
	#extract faces from solids
	for i in geoSet:
		solids = i.SymbolGeometry
		for i in solids:
			faces = i.Faces
	return faces[0]

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

#unwrap surfaces
elements = []
for i in surfaces:
	elements.append(UnwrapElement(i))

if not any(isinstance(item, list) for item in values):
	face = getFace(elements[0])
	#create a spatial field primitive for each face and add to schema
	idx = sfm.AddSpatialFieldPrimitive(face.Reference)
	doubleList = List[float]()
	valList = List[ValueAtPoint]()
	fieldPointsUV = List[Autodesk.Revit.DB.UV]()
	for i,j in zip(values, UVPoints):
		doubleList.Add(float(i))
		valList.Add(ValueAtPoint(doubleList))
		doubleList.Clear()
		fieldPointsUV.Add(j)
	vals = FieldValues(valList)
	pnts = FieldDomainPointsByUV(fieldPointsUV)
	sfm.UpdateSpatialFieldPrimitive(idx, pnts, vals, schemaIndex)
	valList.Clear()
	fieldPointsUV.Clear()
else:
	for element, value, UVPoint in zip(elements, values, UVPoints):
		face = getFace(element)
		idx = sfm.AddSpatialFieldPrimitive(face.Reference)
		doubleList = List[float]()
		valList = List[ValueAtPoint]()
		fieldPointsUV = List[Autodesk.Revit.DB.UV]()
		for i,j in zip(value, UVPoint):
			doubleList.Add(float(i))
			valList.Add(ValueAtPoint(doubleList))
			doubleList.Clear()
			fieldPointsUV.Add(j)
		vals = FieldValues(valList)
		pnts = FieldDomainPointsByUV(fieldPointsUV)
		sfm.UpdateSpatialFieldPrimitive(idx, pnts, vals, schemaIndex)
		valList.Clear()
		fieldPointsUV.Clear()

#create display style for colored surfaces and apply to current view
collector = FilteredElementCollector(doc)
collection = collector.OfClass(AnalysisDisplayStyle).ToElements()
displayStyle = []
for i in collection:
	if i.Name == displayStyleName and i.HasColoredSurfaceSettings():
		displayStyle.append(i)
	elif i.Name == displayStyleName and not i.HasColoredSurfaceSettings():
		message = "Specified Display Style name already \nexists; please supply different name"
	else:
		continue
if len(displayStyle) == 0:
	try:
		analysisDisplayStyle = AnalysisDisplayStyle.CreateAnalysisDisplayStyle(doc, displayStyleName, styleSettings, colorSettings, legendSettings)
	except:
		pass
else:
	analysisDisplayStyle = displayStyle[0]
	analysisDisplayStyle.SetLegendSettings(legendSettings)
	analysisDisplayStyle.SetColorSettings(colorSettings)
	analysisDisplayStyle.SetColoredSurfaceSettings(styleSettings)

try:
	doc.ActiveView.AnalysisDisplayStyleId = analysisDisplayStyle.Id
except:
	pass

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
if message != None:
	OUT = message
else:
	OUT = 0
