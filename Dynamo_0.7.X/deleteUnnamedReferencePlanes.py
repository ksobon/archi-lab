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

#define filter rule (name parameter is empty string)
bip = BuiltInParameter.DATUM_TEXT
provider = ParameterValueProvider(ElementId(bip))
evaluator = FilterStringEquals()
rule = FilterStringRule(provider, evaluator, "", False)
filter = ElementParameterFilter(rule)

#collect all unnamed refernce planes
refPlanes = FilteredElementCollector(doc).OfClass(ReferencePlane).WherePasses(filter).ToElementIds()

# "Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

nDeleted = 0
for i in refPlanes:
	try:
		doc.Delete(i)
		nDeleted += 1
	except:
		pass
		
# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()
	
#Assign your output to the OUT variable
OUT = "Successfully Deleted " + str(nDeleted) + " Unnamed Reference Planes"
