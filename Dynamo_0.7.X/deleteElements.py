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

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
deleteBoolean = IN[1]
#unwrap all elements to use with API
elements = []
for i in IN[0]:
	elements.append(UnwrapElement(i))

idsToDelete = List[Autodesk.Revit.DB.ElementId]()
for i in elements:
	idsToDelete.Add(i.Id)

# "Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

if deleteBoolean:
	doc.Delete(idsToDelete)
	message = "You have successfully deleted \n " + str(idsToDelete.Count) + " elements from Revit model."
else:
	message = "Delete set to false."

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

OUT = '\n'.join('{:^35}'.format(s) for s in message.split('\n'))
