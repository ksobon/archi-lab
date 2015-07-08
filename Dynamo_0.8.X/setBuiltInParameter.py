#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
import sys
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

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
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
import System

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

paramName = IN[0]
paramValues = IN[2]

if isinstance(IN[1], list):
	elements = []
	for i in IN[1]:
		elements.append(UnwrapElement(i))
else:
	elements = IN[1]

def GetBuiltInParam(paramName):
	builtInParams = System.Enum.GetValues(BuiltInParameter)
	test = []
	for i in builtInParams:
		if i.ToString() == paramName:
			test.append(i)
			break
		else:
			continue
	return test[0]

try:
	errorReport = None
	# "Start" the transaction
	TransactionManager.Instance.EnsureInTransaction(doc)
	
	bipName = GetBuiltInParam(paramName)
	for i, j in zip(elements, paramValues):
		param = i.get_Parameter(bipName)
		param.Set(j)
	
	# "End" the transaction
	TransactionManager.Instance.TransactionTaskDone()
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = 0
else:
	OUT = errorReport
