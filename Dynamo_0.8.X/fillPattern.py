#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

# Import ToDSType(bool) extension method
import clr
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

names = IN[0]
target = IN[1]

def GetFillPattern(name, target):
	doc = DocumentManager.Instance.CurrentDBDocument
	fillPat = FillPatternElement.GetFillPatternElementByName(doc, target, name)
	return fillPat.ToDSType(True)

def ProcessListArg(_func, _list, _arg):
	return map( lambda x: ProcessListArg(_func, x, _arg) if type(x)==list else _func(x, _arg), _list )

try:
	errorReport = None
	if isinstance(names, list):
		fillPatterns = ProcessListArg(GetFillPattern, names, target)
	else:
		fillPatterns = GetFillPattern(names, target)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = fillPatterns
else:
	OUT = errorReport
