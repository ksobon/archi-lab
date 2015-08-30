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

doc = DocumentManager.Instance.CurrentDBDocument

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

viewSet = UnwrapElement(IN[0])

viewSets = FilteredElementCollector(doc).OfClass(ViewSheetSet)

for i in viewSets:
	if i.Name == viewSet.Name:
		vs = i
	else:
		continue

#Assign your output to the OUT variable
OUT = [i.ToDSType(True) for i in vs.Views]
