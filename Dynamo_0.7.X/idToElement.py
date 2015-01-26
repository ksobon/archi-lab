#Copyright(c) 2015, Konrad Sobon
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
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
doc = IN[1]

def toRvtId(_id):
	if isinstance(_id, int) or isinstance(_id, str):
		id = ElementId(int(_id))
		return id
	elif isinstance(_id, ElementId):
		return _id

#unwrap incoming information for use with API
ids = []
for i in IN[0]:
    ids.append(UnwrapElement(i))

#use element ids to select elements
elements = []
message = None
try:
	for i in ids:
		elements.append(doc.GetElement(toRvtId(i)).ToDSType(True))
except:
	message = "Invalid Id"
	pass

#Assign your output to the OUT variable
if message != None:
	OUT =  '\n'.join('{:^35}'.format(s) for s in message.split('\n'))
else:
	OUT = elements
