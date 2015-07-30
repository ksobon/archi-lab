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

elem = IN[0]
view = UnwrapElement(IN[1])

if isinstance(elem, list):
	lmnts = []
	for i in elem:
		lmnts.append(UnwrapElement(i))
else:
	lmnts = UnwrapElement(elem)

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
	OUT = "Success!"
else:
	OUT = errorReport
