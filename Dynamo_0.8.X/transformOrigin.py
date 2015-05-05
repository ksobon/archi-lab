#Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)

elements = UnwrapElement(IN[0])

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def GetTransformOrigin(element):
	try:
		return element.GetTransform().Origin.ToPoint()
	except:
		return None
		pass

OUT = ProcessList(GetTransformOrigin, elements)
