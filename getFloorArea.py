#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

elements = []
for i in IN[0]:
	elements.append(UnwrapElement(i))

def process_list(_func, _list):
    return map( lambda x: process_list(_func, x) if type(x)==list else _func(x), _list )

def FloorArea(item):
	paramName = BuiltInParameter.HOST_AREA_COMPUTED
	param = item.get_Parameter(paramName).AsValueString()
	return param

#Assign your output to the OUT variable
OUT = process_list(FloorArea, elements)
