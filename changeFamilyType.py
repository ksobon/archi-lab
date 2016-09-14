# Copyright(c) 2016, Konrad Sobon
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
from RevitServices.Transactions import TransactionManager
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

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def ProcessParallelLists(_func, *lists):
	return map( lambda *xs: ProcessParallelLists(_func, *xs) if all(type(x) is list for x in xs) else _func(*xs), *lists )

def ProcessListArg(_func, _list, _arg):
    return map( lambda x: ProcessListArg(_func, x, _arg) if type(x)==list else _func(x, _arg), _list )

def Unwrap(item):
	return UnwrapElement(item)

def ChangeType(element, typeId):
	element.ChangeTypeId(ElementId(typeId))
	return element

if isinstance(IN[0], list):
	elements = ProcessList(Unwrap, IN[0])
else:
	elements = [Unwrap(IN[0])]

typeIds = IN[1]

try:
	errorReport = None
	TransactionManager.Instance.EnsureInTransaction(doc)
	if isinstance(typeIds, list):
		output = ProcessParallelLists(ChangeType, elements, typeIds)
	else:
		output = ProcessListArg(ChangeType, elements, typeIds)
	TransactionManager.Instance.TransactionTaskDone()
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

# End Transaction
TransactionManager.Instance.TransactionTaskDone()


#Assign your output to the OUT variable
if errorReport == None:
	OUT = output
else:
	OUT = errorReport
