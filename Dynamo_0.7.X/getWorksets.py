#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
from Autodesk.Revit.DB import *
clr.ImportExtensions(Revit.Elements)

#The inputs to this node will be stored as a list in the IN variable.
#doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
doc = IN[0]

#create workset collector
userWorksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
#extract workset's name and ids
names, ids = [], []
for i in userWorksets:
	names.append(i.Name)
	ids.append(i.Id)
	
#Assign your output to the OUT variable
OUT = userWorksets, names, ids
