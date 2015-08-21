#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

# Import DocumentManager and TransactionManager
import clr
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

typeNames = IN[0]

def ProcessList(_func, _list):
	return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def GetTextNoteType(typeName):
	doc = DocumentManager.Instance.CurrentDBDocument
	textNoteTypes = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
	bip = BuiltInParameter.ALL_MODEL_TYPE_NAME
	for i in textNoteTypes:
		if i.get_Parameter(bip).AsString() != typeName:
			continue
		else:
			return i
			break
try:
	errorReport = None
	if isinstance(typeNames, list):
		textTypes = ProcessList(GetTextNoteType, typeNames)
	else:
		textTypes = GetTextNoteType(typeNames)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()
	
#Assign your output to the OUT variable
if errorReport == None:
	OUT = textTypes
else:
	OUT = errorReport
