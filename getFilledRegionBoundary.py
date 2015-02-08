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
from Autodesk.Revit.DB.Analysis import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import ToProtoType, ToRevitType geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
filledRegions = UnwrapElement(IN[0])

def process_list(_func, _list):
    return map( lambda x: process_list(_func, x) if type(x)==list else _func(x), _list )

def ToDSType(item):
	curves = []
	for i in item:
		curves.append(i.ToProtoType())
	return curves

curves = []
for i in filledRegions:
	curves.append(process_list(ToDSType, i.GetBoundaries()))

#Assign your output to the OUT variable
OUT = curves
