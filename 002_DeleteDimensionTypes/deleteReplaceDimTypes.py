#Copyright(c) 2015, Konrad K Sobon
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

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

sReplace = IN[0]
sReplaceWith = IN[1]
boolean = IN[2]

dims = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType().ToElements()

def ProcessList(_func, _list):
	return map(lambda x: ProcessList(_func, x) if type(x) == list else _func(x), _list)

def GetDimType(name):
	dims = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType().ToElements()
	dimNames = [i.Name for i in dims]
	for i, j in zip(dims, dimNames):
		if j == name:
			return i
		else:
			return None

replacementTypes = ProcessList(GetDimType, sReplace)

#"Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

for index in range(0, len(dims), 1):
	item = dims[index]
	if item.ToDSType(True).Name in sReplace:
		replaceWith = replacementTypes[sReplace.index(item.ToDSType(True).Name)]		
		try:
			item.DimensionType = replaceWith
		except:
			pass
	else:
		continue

dTypes = FilteredElementCollector(doc).OfClass(DimensionType)
sTypes = FilteredElementCollector(doc).OfClass(SpotDimensionType)

sTypesName = []
for i in sTypes:
	sTypesName.append(i.ToDSType(True).Name)

dimensionTypes = []
for i in dTypes:
	if i.ToDSType(True).Name not in sTypesName:
		dimensionTypes.append(i)


idsToDelete = List[Autodesk.Revit.DB.ElementId]()
if boolean == True:
	for name in sReplace:
		try:
			idsToDelete.Add(next(i.Id for i in dimensionTypes if name==i.ToDSType(True).Name))
		except StopIteration:
			continue	
try:
	doc.Delete(idsToDelete)
except:
	pass

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

if boolean == True:
	message = "You have successfully replaced \n and deleted all of the specified \n dimension types."
else:
	message = "You have successfully replaced \n all of the specified dimension types."

OUT = '\n'.join('{:^35}'.format(s) for s in message.split('\n'))
