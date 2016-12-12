# Copyright(c) 2016, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

# Import DocumentManager
import clr
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
from Autodesk.Revit.DB import *
clr.ImportExtensions(Revit.Elements)

doc = DocumentManager.Instance.CurrentDBDocument

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.

try:
	errorReport = None
	userWorksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
	names, ids = [], []
	for i in userWorksets:
		names.append(i.Name)
		ids.append(i.Id)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = userWorksets, names, ids
else:
	OUT = errorReport
