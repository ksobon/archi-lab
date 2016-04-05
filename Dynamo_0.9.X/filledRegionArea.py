# Copyright(c) 2016, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

# Import RevitAPI
import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

filledRegions = UnwrapElement(IN[0])

#Assign your output to the OUT variable
OUT = [i.get_Parameter(BuiltInParameter.HOST_AREA_COMPUTED).AsDouble() for i in filledRegions]
