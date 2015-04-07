#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

views = UnwrapElement(IN[0])
viewTempName = IN[1]
runMe = IN[2]

def ApplyViewTemplate(view, template):
	view.ViewTemplateId = template.Id
	return view

def ProcessListArg(_func, _list, _arg):
	return map( lambda x: processListArg(_func, x, _arg) if type(x)==list else _func(x, _arg), _list )

if runMe:
	collector = FilteredElementCollector(doc).OfClass(View)
	for i in collector:
		if i.IsTemplate == True and i.Name == viewTempName:
			viewTemp = i
	
	# "Start" the transaction
	TransactionManager.Instance.EnsureInTransaction(doc)
	
	#Assign your output to the OUT variable
	OUT = ProcessListArg(ApplyViewTemplate, views, viewTemp)
	
	# "End" the transaction
	TransactionManager.Instance.TransactionTaskDone()
else:
	OUT = "Run Me set to False"
