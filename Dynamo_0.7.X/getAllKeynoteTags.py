#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.BuiltInCategory import *

doc = DocumentManager.Instance.CurrentDBDocument

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

elementList = FilteredElementCollector(doc).OfCategory(OST_KeynoteTags).WhereElementIsNotElementType().ToElements()

#Assign your output to the OUT variable
OUT = elementList
