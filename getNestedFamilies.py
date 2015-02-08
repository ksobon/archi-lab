#Copyright(c) 2014, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

from System.Collections.Generic import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

#unwrap all elements to use with API
elements = []
for i in IN[0]:
	elements.append(UnwrapElement(i))

def search_things(things):
	names = []
	for thing in things:
		if not thing.GetSubComponentIds():
			names.append(thing)
		else:
			names.append(search_things(idsToElements(thing.GetSubComponentIds())))
	return names

def idsToElements(ids):
	return map(doc.GetElement, ids)

#Assign your output to the OUT variable
OUT = search_things(elements)
