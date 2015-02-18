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

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
levelName = IN[0]

level = None
message = "Name doesn't match any levels in \n the project. Pick a different one"
allLevels = FilteredElementCollector(doc).OfClass(Level).ToElements()
for i in allLevels:
	if i.Name == levelName:
		level = i
		break
	else:
		continue

if level == None:
	OUT = '\n'.join('{:^35}'.format(s) for s in message.split('\n'))
else:
	OUT = level
