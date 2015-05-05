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

import System
from System import Array
from System.Collections.Generic import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

category = IN[0]
level = IN[1]

def toRvtId(_id):
	if isinstance(_id, int) or isinstance(_id, str):
		id = ElementId(int(_id))
		return id
	elif isinstance(_id, ElementId):
		return _id

bic = System.Enum.ToObject(BuiltInCategory, category.Id)
levelFilter = ElementLevelFilter(toRvtId(level.Id))
instances = FilteredElementCollector(doc).OfCategory(bic).WherePasses(levelFilter).WhereElementIsNotElementType().ToElements()

#Assign your output to the OUT variable
OUT = instances
