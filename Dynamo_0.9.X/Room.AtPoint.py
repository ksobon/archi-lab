# Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

def Unwrap(item):
	return UnwrapElement(item)

def GetRoomAtPoint(pt):
	doc = DocumentManager.Instance.CurrentDBDocument
	return doc.GetRoomAtPoint(pt.ToXyz())

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )
    
if isinstance(IN[0], list):
	points = ProcessList(Unwrap, IN[0])
else:
	points = [Unwrap(IN[0])]

try:
	errorReport = None
	result = ProcessList(GetRoomAtPoint, points)

except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = result
else:
	OUT = errorReport
