#Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

# This node is based on Julien Benoit's Element.GetElementFromLinkedFile 
# node. Some slight improvements were made removing unnecessary imports/references.
# Big thank you to Julien for sharing his work. 

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import System

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

_linkDoc = IN[0]
_category = IN[1]

filter = ElementCategoryFilter(System.Enum.ToObject(BuiltInCategory, _category.Id))

OUT = FilteredElementCollector(_linkDoc).WherePasses(filter).WhereElementIsNotElementType().ToElements()
