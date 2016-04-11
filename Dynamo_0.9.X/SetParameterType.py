# Copyright(c) 2016, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

# Import Element wrapper extension methods
import clr
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

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

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def ProcessParallelLists(_func, *lists):
	return map( lambda *xs: ProcessParallelLists(_func, *xs) if all(type(x) is list for x in xs) else _func(*xs), *lists )

def Unwrap(item):
	return UnwrapElement(item)

def ApplyParam(e, pv, pn):
	eType = doc.GetElement(e.GetTypeId())
	params = eType.Parameters
	for i in params:
		if i.Definition.Name == pn:
			i.Set(pv)
		else:
			continue
	return e

elements = []
if hasattr(IN[0], "__iter__"):
	elements = ProcessList(Unwrap(IN[0]))
else:
	elements = [Unwrap(IN[0])]

if hasattr(IN[1], "__iter__"):
	paramNames = IN[1]
else:
	paramNames = [IN[1]]

if hasattr(IN[2], "__iter__"):
	paramValues = IN[2]
else:
	paramValues = [IN[2]]

try:
	errorReport = None
	TransactionManager.Instance.EnsureInTransaction(doc)
	output = ProcessParallelLists(ApplyParam, elements, paramValues, paramNames)
	TransactionManager.Instance.TransactionTaskDone()
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = output
else:
	OUT = errorReport
