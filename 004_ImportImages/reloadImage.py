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

doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

filePath = IN[0]
runIt = IN[1]

if runIt:
	tempName = filePath.split("\\")
	elementName = tempName[len(tempName)-1]
	
	imgs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RasterImages).WhereElementIsElementType().ToElements()
	
	for i in imgs:
		if i.ToDSType(True).Name == elementName:
			imageOut = i
			break
		else:
			continue
	
	TransactionManager.Instance.EnsureInTransaction(doc)
	imageOut.Reload()
	TransactionManager.Instance.TransactionTaskDone()
	message = "Success!"
else:
	message = "Set RunIt to True."
#Assign your output to the OUT variable
OUT = message
