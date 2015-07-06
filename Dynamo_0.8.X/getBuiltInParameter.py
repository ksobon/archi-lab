#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

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

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

paramNames = IN[0]

if isinstance(IN[1], list):
	sheets = []
	for i in IN[1]:
		sheets.append(UnwrapElement(i))
else:
	sheets = IN[1]

elements = []
for i in sheets:
	elements.append(UnwrapElement(i))

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def ProcessListArg(_func, _list, _arg):
    return map( lambda x: ProcessListArg(_func, x, _arg) if type(x)==list else _func(x, _arg), _list )

def GetBuiltInParam(paramName):
	builtInParams = System.Enum.GetValues(BuiltInParameter)
	test = []
	for i in builtInParams:
		if i.ToString() == paramName:
			test.append(i)
			break
		else:
			continue
	return test[0]

def GetBipValue(element, bip):
	value = element.get_Parameter(bip).AsString()
	return value

paramValues = []
if isinstance(paramNames, list):
	builtInParams = ProcessList(GetBuiltInParam, paramNames)
	for i in builtInParams:
		paramValues.append(ProcessListArg(GetBipValue, elements, i))
else:
	builtInParams = GetBuiltInParam(paramNames)
	if isinstance(sheets, list):
		for sheet in sheets:
			paramValues.append(GetBipValue(sheet, builtInParams))

#Assign your output to the OUT variable
OUT = paramValues
