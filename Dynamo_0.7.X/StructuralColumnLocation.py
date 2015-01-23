#Copyright(c) 2015, Konrad Sobon
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

rvtPoints = [UnwrapElement(i).Location for i in IN[0]]

#Assign your output to the OUT variable
OUT = [Autodesk.DesignScript.Geometry.Point.ByCoordinates(i.Point.X, i.Point.Y, i.Point.Z) for i in rvtPoints]
