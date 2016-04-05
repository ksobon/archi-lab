# Copyright(c) 2016, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

# Import ToDSType(bool) extension method
import clr
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

from System.Collections.Generic import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def Unwrap(item):
	return UnwrapElement(item)

def ToRevitId(_id):
	if isinstance(_id, int):
		id = ElementId(int(_id))
		return ("ElementId", id)
	elif isinstance(_id, basestring) and len(_id) > 8:
		return ("GUID", _id)
	elif isinstance(_id, basestring) and len(_id) < 8:
		id = ElementId(int(_id))
		return ("ElementId", id)
	elif isinstance(_id, Autodesk.Revit.DB.ElementId):
		return ("ElementId", _id)
	else:
		return None

def ProcessIds(_id):
	id = ToRevitId(_id)
	if id == None:
		return None
	elif id[0] == "ElementId":
		try:
			return doc.GetElement.Overloads[Autodesk.Revit.DB.ElementId](id[1]).ToDSType(True)
		except:
			return None
	else:
		try:
			return doc.GetElement.Overloads[str](id[1]).ToDSType(True)
		except:
			return None

#unwrap incoming information for use with API
if isinstance(IN[0], list):
	ids = ProcessList(Unwrap, IN[0])
else:
	ids = [Unwrap(IN[0])]
    
try:
	errorReport = None
	elements = []
	output = ProcessList(ProcessIds, ids)
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
	OUT = output
else:
	OUT = errorReport
