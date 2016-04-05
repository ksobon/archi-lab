# Copyright(c) 2016, Konrad K Sobon
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

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def GetElement(id):
	doc = DocumentManager.Instance.CurrentDBDocument
	return doc.GetElement(id)

if isinstance(IN[0], list):
	sheets = []
	for i in IN[0]:
		sheets.append(UnwrapElement(i))
else:
	sheets = [UnwrapElement(IN[0])]

try:
	errorReport = None
	revIds = []
	for i in sheets:
		revIds.append(list(i.GetAllRevisionIds()))
	revisions = ProcessList(GetElement, revIds)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = revisions
else:
	OUT = errorReport
