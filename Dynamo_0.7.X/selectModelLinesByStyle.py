# Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.BuiltInCategory import *

doc = DocumentManager.Instance.CurrentDBDocument

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

styleName = IN[0]

try:
	errorReport = None
	collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines)
	modelLines = []
	for i in collector:
		if i.Name == "Model Lines" and i.LineStyle.Name == styleName:
			modelLines.append(i)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()
	
#Assign your output to the OUT variable
if errorReport == None:
	OUT = modelLines
else:
	OUT = errorReport
