# Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

# Import Element wrapper extension methods
import clr
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

def Unwrap(item):
	return UnwrapElement(item)

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

if isinstance(IN[0], list):
	elements = ProcessList(Unwrap, IN[0])
else:
	elements = [Unwrap(IN[0])]

elemType = IN[1]

def IsOfType(item, category = elemType):
	if item != None:
		if item.GetType() == category:
			return True
		else:
			return False
	else:
		return False

try:
	errorReport = None
	output = ProcessList(IsOfType, elements)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = output
else:
	OUT = errorReport
