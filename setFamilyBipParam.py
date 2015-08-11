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
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
import System

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

paths = IN[0]
paramName = IN[1]
value = IN[2]

class FamilyOption(IFamilyLoadOptions):
	def OnFamilyFound(self, familyInUse, overwriteParameterValues):
		overwriteParameterValues = True
		return True

	def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
		return True

def GetBuiltInParam(paramName):
	builtInParams = System.Enum.GetValues(BuiltInParameter)
	test = []
	for i in builtInParams:
		if i.ToString() == paramName:
			test.append(i)
			break
		else:
			continue
	if len(test) == 0:
		return None
	else:
		return test[0]

try:
	errorReport = None
	outValue = []
	for i in paths:
		if "rfa" in i:
			famDoc = app.OpenDocumentFile(i)
			ownerFamily = famDoc.OwnerFamily
			bip = GetBuiltInParam(paramName)
			param = ownerFamily.get_Parameter(bip)
			TransactionManager.Instance.EnsureInTransaction(famDoc)
			param.Set(value)
			TransactionManager.Instance.TransactionTaskDone()
			outValue.append(famDoc.LoadFamily(doc, FamilyOption()))
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = outValue
else:
	OUT = errorReport
