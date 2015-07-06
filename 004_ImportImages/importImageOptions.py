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

placement = IN[0]
refPt = IN[1]
res = IN[2]

iio = ImageImportOptions()

def toRvtPoint(point):
	x = point.X
	y = point.Y
	z = point.Z
	return XYZ(x,y,z)

message = None
if placement != None:
	iio.Placement = placement
if refPt != None:
	iio.RefPoint = toRvtPoint(refPt)
else:
	message = "Please specify placement point."
if res != None:
	iio.Resolution = res
else:
	iio.Resolution = 72

#Assign your output to the OUT variable
OUT = iio
