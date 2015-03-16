#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

elist = IN[0]
nameInput = str(IN[1])

elements = []
outList = []

for i in range(0,len(elist)):
    elements.append(UnwrapElement(elist[i]))

for i in elements:
	elemType = doc.GetElement(i.GetTypeId())
	params = elemType.Parameters
	for i in params:
		if i.Definition.Name == nameInput:
			outList.append(i.AsString())
		else:
			continue

OUT = outList
