#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

# Import DocumentManager and TransactionManager
import clr
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

try:
	errorReport = None
	dTypes = FilteredElementCollector(doc).OfClass(DimensionType)
	sTypes = FilteredElementCollector(doc).OfClass(SpotDimensionType)
	
	sTypesName = []
	for i in sTypes:
		sTypesName.append(i.ToDSType(True).Name)
	
	dimensionTypes = []
	for i in dTypes:
		if i.ToDSType(True).Name not in sTypesName:
			dimensionTypes.append(i.ToDSType(True))
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()
	
#Assign your output to the OUT variable
if errorReport == None:
	OUT = dimensionTypes
else:
	OUT = errorReport
