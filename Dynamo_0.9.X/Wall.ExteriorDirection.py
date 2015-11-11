# Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def Unwrap(item):
	return UnwrapElement(item)

def GetExteriorWallDirection(item):
	if type(item) == Autodesk.Revit.DB.Wall:
		locationCurve = item.Location
		if locationCurve != None:
			curve = locationCurve.Curve
			direction = XYZ.BasisX
			if type(curve) == Autodesk.Revit.DB.Line:
				direction = curve.ComputeDerivatives(0, True).BasisX.Normalize()
			else:
				direction = (curve.GetEndPoint(1) - curve.GetEndPoint(0)).Normalize()
			exteriorDirection = XYZ.BasisZ.CrossProduct(direction)
			
			if item.Flipped:
				exteriorDirection = -exteriorDirection
			return exteriorDirection.ToVector()
	else:
		return "Not a Wall"

if isinstance(IN[0], list):
	walls = ProcessList(Unwrap, IN[0])
else:
	walls = [UnwrapElement(IN[0])]

try:
	errorReport = None
	output = ProcessList(GetExteriorWallDirection, walls)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()


#Assign your output to the OUT variable
if errorReport == None:
	OUT = output
else:
	OUT = errorReport
