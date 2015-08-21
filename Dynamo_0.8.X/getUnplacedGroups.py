#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

# Import DocumentManager and TransactionManager
import clr
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

try:
	errorReport = None
	groups = FilteredElementCollector(doc).OfClass(GroupType)
	unplacedGroups = []
	for i in groups:
		gInstances = i.Groups
		if gInstances.IsEmpty:
			unplacedGroups.append(i)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = unplacedGroups
else:
	OUT = errorReport
