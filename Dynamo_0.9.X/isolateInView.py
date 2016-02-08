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

import System
from System import Array
from System.Collections.Generic import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

view = UnwrapElement(IN[1])

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def Unwrap(item):
	try:
		e = doc.GetElement(ElementId(int(item.Id)))
		return e
	except:
		return None

def ClearList(_list):
    out = []
    for _list1 in _list:
        if _list1 is None:
            continue
        if not _list1:
        	continue
        if isinstance(_list1, list):
             _list1 = ClearList(_list1)
             if not _list1:
                 continue
        out.append(_list1)
    return out

if isinstance(IN[0], list):
	lmnts = ProcessList(Unwrap, IN[0])
	lmnts = ClearList(lmnts)
else:
	lmnts = [Unwrap(elem)]
	lmnts = ClearList(lmnts)

try:
	errorReport = None
	elemSet = ElementSet()
	for i in lmnts:
		elemSet.Insert(i)
	
	excludes = List[ElementId]()
	elemIter = elemSet.ForwardIterator()
	elemIter.Reset()
	while elemIter.MoveNext():
		curElem = elemIter.Current
		excludes.Add(curElem.Id)
	
	filter = ExclusionFilter(excludes)
	
	new_collector = FilteredElementCollector(doc, view.Id).WhereElementIsNotElementType().WherePasses(filter).ToElementIds()
	TransactionManager.Instance.EnsureInTransaction(doc)
	view.HideElementsTemporary(new_collector)
	TransactionManager.Instance.TransactionTaskDone()

except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()	

#Assign your output to the OUT variable
if errorReport == None:
	OUT = lmnts
else:
	OUT = errorReport
