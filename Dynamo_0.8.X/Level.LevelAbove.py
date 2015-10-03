#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

if isinstance(IN[0], list):
	levels = IN[0]
else:
	levels = [IN[0]]

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def GetLevelAbove(e):
	doc = DocumentManager.Instance.CurrentDBDocument
	allLevels = FilteredElementCollector(doc) \
				.OfCategory(BuiltInCategory.OST_Levels) \
				.WhereElementIsNotElementType() \
				.ToElements()

	elevations = [i.Elevation for i in allLevels]
	sortedLevels = [x for (y,x) in sorted(zip(elevations,allLevels))]
	sortedLevelNames = [i.Name for i in sortedLevels]
	index = sortedLevelNames.index(e.Name)
	return sortedLevels[index+1]

try:
	errorReport = None
	output = ProcessList(GetLevelAbove, levels)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = output
else:
	OUT = errorReport
