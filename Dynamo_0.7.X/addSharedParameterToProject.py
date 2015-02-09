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
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

from System.Collections.Generic import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
import System
#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

_paramName = IN[0]
_groupName = IN[1]
_paramType = IN[2]
_visible = IN[3]
_category = IN[4]
_paramGroup = IN[5]
_instance = IN[6]

def ParamBindingExists(_doc, _paramName, _paramType):
	map = doc.ParameterBindings
	iterator = map.ForwardIterator()
	iterator.Reset()
	while iterator.MoveNext():
		if iterator.Key != None and iterator.Key.Name == _paramName and iterator.Key.ParameterType == _paramType:
			paramExists = True
			break
		else:
			paramExists = False
	return paramExists

def RemoveParamBinding(_doc, _paramName, _paramType):
	map = doc.ParameterBindings
	iterator = map.ForwardIterator()
	iterator.Reset()
	while iterator.MoveNext():
		if iterator.Key != None and iterator.Key.Name == _paramName and iterator.Key.ParameterType == _paramType:
			definition = iterator.Key
			break
	message = None
	if definition != None:
		map.Remove(definition)
		message = "Success"
	return message

def addParam(doc, _paramName, _visible, _instance, _groupName, _paramGroup):
	message = None
	if ParamBindingExists(doc, _paramName, _paramType):
		if not RemoveParamBinding(doc, _paramName, _paramType) == "Success":
			message = "Param Binding Not Removed Successfully"
		else:
			message = None
			
	group = file.Groups.get_Item(_groupName)
	if group == None:
		group = file.Groups.Create(_groupName)
	if group.Definitions.Contains(group.Definitions.Item[_paramName]):
		_def = group.Definitions.Item[_paramName]
	else:
		_def = group.Definitions.Create(_paramName, _paramType, _visible)
	
	param = doc.ParameterBindings.Insert(_def, bind, _paramGroup)
	return message
#"Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

try:
	file = app.OpenSharedParameterFile()
except:
	message = "No Shared Parameter file found."
	pass

builtInCategory = System.Enum.ToObject(BuiltInCategory, _category.Id)
cats = app.Create.NewCategorySet()
cats.Insert(doc.Settings.Categories.get_Item(builtInCategory))
if _instance:
	bind = app.Create.NewInstanceBinding(cats)
else:
	bind = app.Create.NewTypeBinding(cats)


if isinstance(_paramName, list):
	for i, j, k in zip(_paramName, _visible, _instance):
		message = addParam(doc, i, j, k, _groupName, _paramGroup)
else:
	message = addParam(doc, _paramName, _visible, _instance, _groupName, _paramGroup)


# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

#Assign your output to the OUT variable
if message == None:
	OUT = "Success"
else:
	OUT = message
