#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

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

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

filePath = IN[0]
iio = IN[1]
view = UnwrapElement(IN[2])
RunIt = IN[3]

if RunIt:
	# Start Transaction
	doc = DocumentManager.Instance.CurrentDBDocument
	TransactionManager.Instance.EnsureInTransaction(doc)
	
	newElement = clr.StrongBox[Element]()
	elementOut = doc.Import(file = str(filePath), options = iio, view = view, element = newElement)
	
	# End Transaction
	TransactionManager.Instance.TransactionTaskDone()
	message = "Success!"
else:
	message = "Set RunIt to True."

#Assign your output to the OUT variable
if message == "Success!":
	OUT = elementOut
else:
	OUT = message
