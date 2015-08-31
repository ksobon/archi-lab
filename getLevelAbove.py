#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
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
doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

levels = IN[0]

allLevels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
elevations = [i.Elevation for i in allLevels]

sortedLevels = [x for (y,x) in sorted(zip(elevations,allLevels))]
sortedLevelNames = [i.Name for i in sortedLevels]

output = []
for i in levels:
	index = sortedLevelNames.index(i.Name)
	output.append(sortedLevels[index+1])
#Assign your output to the OUT variable.
OUT = output
