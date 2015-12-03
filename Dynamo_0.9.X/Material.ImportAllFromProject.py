# Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

# Import Element wrapper extension methods
import clr
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

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
RunIt = IN[1]

class CustomCopyHandler(IDuplicateTypeNamesHandler):
	def OnDuplicateTypeNamesFound(self, args):
		return DuplicateTypeAction.UseDestinationTypes

try:
	if RunIt:
		TransactionManager.Instance.EnsureInTransaction(doc)
		errorReport = None
		fileDoc = app.OpenDocumentFile(IN[0])
		filter = ElementClassFilter(Material)
		allMat = FilteredElementCollector(fileDoc).WherePasses(filter).ToElementIds()
		trans = Autodesk.Revit.DB.Transform.Identity
		co = CopyPasteOptions()
		co.SetDuplicateTypeNamesHandler(CustomCopyHandler())
		newIds = ElementTransformUtils.CopyElements(fileDoc, allMat, doc, trans, co)
		output = []
		if newIds != None:
			for i in newIds:
				output.append(doc.GetElement(i).ToDSType(False))
		TransactionManager.Instance.TransactionTaskDone()
	else:
		errorReport = "Set Run it to true!"
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = output
else:
	OUT = errorReport
