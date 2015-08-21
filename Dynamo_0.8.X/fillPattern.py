#Copyright(c) 2015, Konrad Sobon
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

name = str(IN[0])
target = IN[1]

try:
	errorReport = None
	fillPat = FillPatternElement.GetFillPatternElementByName(doc, target, name)
	fillPat = fillPat.ToDSType(True)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = fillPat
else:
	OUT = errorReport
