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
	revs = []
	for i in IN[0]:
		revs.append(UnwrapElement(i))
else:
	revs = [UnwrapElement(IN[0])]

try:
	errorReport = None
	sequence = [i.SequenceNumber for i in revs]
	date = [i.RevisionDate for i in revs]
	issuedTo = [i.IssuedTo for i in revs]
	issuedBy = [i.IssuedBy for i in revs]
	issued = [i.Issued for i in revs]
	description = [i.Description for i in revs]
	
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = [sequence, date, description, issued, issuedTo, issuedBy]
else:
	OUT = errorReport
