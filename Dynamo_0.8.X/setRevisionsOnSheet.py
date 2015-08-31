# Copyright(c) 2015, Konrad K Sobon
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
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import System
from System import Array
from System.Collections.Generic import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

if isinstance(IN[0], list):
	sheets = []
	for i in IN[0]:
		sheets.append(UnwrapElement(i))
else:
	sheets = [UnwrapElement(IN[0])]

if isinstance(IN[1], list):
	revs = []
	for i in IN[1]:
		revs.append(UnwrapElement(i))
else:
	revs = [UnwrapElement(IN[1])]
	
RunIt = IN[2]

if RunIt:
	try:
		errorReport = None
		for i in sheets:
			revisionsOnSheet = i.GetAdditionalRevisionIds()
			for r in revs:
				if r.Id not in revisionsOnSheet:
					revisionsOnSheet.Add(r.Id)
				else:
					continue
			TransactionManager.Instance.EnsureInTransaction(doc)
			i.SetAdditionalRevisionIds(revisionsOnSheet)
			TransactionManager.Instance.TransactionTaskDone()
			
	except:
		# if error accurs anywhere in the process catch it
		import traceback
		errorReport = traceback.format_exc()
else:
	errorReport = "Set RunIt to True."


#Assign your output to the OUT variable
if errorReport == None:
	OUT = IN[0]
else:
	OUT = errorReport
