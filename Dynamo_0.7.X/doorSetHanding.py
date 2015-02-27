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

#unwrap inputs
elements = []
for i in IN[0]:
	elements.append(UnwrapElement(i))
phase = UnwrapElement(IN[1])

#check if door has a left or right handed swing
right, left, lhr, rhr = [], [], [], []
for i in elements:
	to_room = i.ToRoom[phase]
	if to_room is not None:
		if not i.FacingFlipped:
			if i.HandFlipped:
				right.append(i)
			else:
				left.append(i)
		else:
			if i.HandFlipped:
				left.append(i)
			else:
				right.append(i)
	else:
		if i.FacingFlipped:
			if i.HandFlipped:
				rhr.append(i)
			else:
				lhr.append(i)
		else:
			if i.HandFlipped:
				lhr.append(i)
			else:
				rhr.append(i)

#Assign your output to the OUT variable
OUT = right, left, rhr, lhr
