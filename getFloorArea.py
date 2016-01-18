# Copyright(c) 2016, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

# Import RevitAPI
import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

def Unwrap(item):
	return UnwrapElement(item)

def ProcessList(_func, _list):
    return map( lambda x: process_list(_func, x) if type(x)==list else _func(x), _list )

def FloorArea(item):
	return item.get_Parameter(BuiltInParameter.HOST_AREA_COMPUTED).AsValueString()

if isinstance(IN[0], list):
	elements = ProcessList(Unwrap, IN[0])
else:
	elements = [Unwrap(IN[0])]

#Assign your output to the OUT variable
OUT = ProcessList(FloorArea, elements)
